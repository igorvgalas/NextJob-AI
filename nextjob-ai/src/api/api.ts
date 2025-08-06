import {
  useMutation,
  useQuery,
  UseMutationOptions,
  UseQueryOptions,
  UseQueryResult,
  UseMutationResult,
  useQueryClient,
} from '@tanstack/react-query';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { refreshToken } from '../hooks/useRefreshToken';
import Constants from 'expo-constants';

export class ApiError extends Error {
  constructor(public response: Response) {
    super(`API Error ${response.status}`);
  }
}

export interface JWTApiResult {
  access: string;
  refresh: string;
}

export interface FetchArgs {
  url: string;
  options: any;
}
const fetchurl = Constants.expoConfig.extra.BASE_URL;
async function queryApi<ApiResult>(
  fetchArgs: FetchArgs,
  headers: Headers
): Promise<ApiResult> {
  let token = await AsyncStorage.getItem('token');
  headers.set('Content-Type', 'application/json');
  if (token) {
    headers.set('Authorization', `Bearer ${token}`);
  }

  let response = await fetch(fetchurl + fetchArgs.url, {
    ...fetchArgs.options,
    body: fetchArgs.options.body && JSON.stringify(fetchArgs.options.body),
    headers,
  });

  let retries = 0;
  while (response.status === 401 && retries < 3) {
    const newToken = await refreshToken();
    if (!newToken) {
      await AsyncStorage.multiRemove(['token', 'refreshToken']);
      break;
    }
    token = newToken;
    const retryHeaders = new Headers();
    retryHeaders.set('Content-Type', 'application/json');
    retryHeaders.set('Authorization', `Bearer ${newToken}`);
    response = await fetch(fetchurl + fetchArgs.url, {
      ...fetchArgs.options,
      body: fetchArgs.options.body && JSON.stringify(fetchArgs.options.body),
      headers: retryHeaders,
    });
    retries++;
  }
  if (response.status === 401) {
    await AsyncStorage.multiRemove(['token', 'refreshToken']);
    throw new Error('Unauthorized and refresh failed');
  }

  if (response.status === 204) {
    return {} as ApiResult;
  }

  const json = (await response.json()) as Readonly<ApiResult>;

  if (response.status < 200 || response.status >= 300) {
    throw json;
  }

  return json;
}

function useApi<ApiResult, ErrorType = unknown>(
  fetchArgs: FetchArgs,
  options?: UseQueryOptions<ApiResult, ErrorType, ApiResult>,
  queryKey?: Array<string | Array<string | number | boolean | null>>
): UseQueryResult<ApiResult, ErrorType> {
  const baseCacheKey = [JSON.stringify([fetchArgs.url, fetchArgs.options])];
  const cacheKey = queryKey
    ? [...queryKey.flatMap((key) => (typeof key === 'string' ? [key] : key)), ...baseCacheKey]
    : baseCacheKey;

  return useQuery<ApiResult, ErrorType, ApiResult>({
    queryKey: cacheKey,
    queryFn: () => queryApi<ApiResult>(fetchArgs, new Headers()),
    ...options,
  });
}

function useApiMutation<ApiResource, ApiResponse = undefined>(
  mutation: (resource: ApiResource) => FetchArgs,
  options?: UseMutationOptions<ApiResponse, Error, ApiResource, unknown>,
  invalidateKeys?: (string | number | boolean | null)[]
): UseMutationResult<ApiResponse, Error, ApiResource, unknown> {
  const queryClient = useQueryClient();

  return useMutation<ApiResponse, Error, ApiResource>({
    mutationFn: async (data: ApiResource) => {
      return queryApi<ApiResponse>(mutation(data), new Headers());
    },
    ...options,
    onSuccess: (...args) => {
      if (invalidateKeys) {
        invalidateKeys.forEach(key => queryClient.invalidateQueries({ queryKey: [key] }));
      }
      options?.onSuccess?.(...args);
    },
    onError: (error, variables, context) => {
      if (invalidateKeys) {
        invalidateKeys.forEach(key => queryClient.invalidateQueries({ queryKey: [key] }));
      }
      options?.onError?.(error, variables, context);
    },
  });
}

export {
  useApi,
  useApiMutation,
  queryApi,
};