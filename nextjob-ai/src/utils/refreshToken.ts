import AsyncStorage from '@react-native-async-storage/async-storage';
import Constants from 'expo-constants';

let isRefreshing = false;
let refreshQueue: Array<{
  resolve: (value?: string | PromiseLike<string>) => void;
  reject: (reason?: any) => void;
}> = [];

export const refreshToken = async (): Promise<string> => {
  if (isRefreshing) {
    return new Promise((resolve, reject) => {
      refreshQueue.push({ resolve, reject });
    });
  }

  isRefreshing = true;

  const refreshToken = await AsyncStorage.getItem('refreshToken');
  if (!refreshToken) {
    isRefreshing = false;
    throw new Error('No refresh token available');
  }

  try {
    const response = await fetch(`${Constants.expoConfig.extra.BASE_URL}/auth/jwt/refresh`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ refresh: refreshToken }),
    });

    if (!response.ok) {
      const errorData = await response.json();
      await AsyncStorage.removeItem('token');
      await AsyncStorage.removeItem('refreshToken');

      while (refreshQueue.length > 0) {
        const { reject } = refreshQueue.shift()!;
        reject(errorData.detail || 'Token refresh failed');
      }

      throw new Error(errorData.detail || 'Token refresh failed');
    }

    const data = await response.json();
    await AsyncStorage.setItem('token', data.access);

    while (refreshQueue.length > 0) {
      const { resolve } = refreshQueue.shift()!;
      resolve(data.access);
    }

    return data.access;
  } catch (error) {
    console.error('Token refresh error:', error);

    await AsyncStorage.removeItem('token');
    await AsyncStorage.removeItem('refreshToken');

    while (refreshQueue.length > 0) {
      const { reject } = refreshQueue.shift()!;
      reject(error);
    }

    throw error;
  } finally {
    isRefreshing = false;
  }
};
