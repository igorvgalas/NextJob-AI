import React, { useEffect, useState, createContext, useContext } from "react";
import { ContextProvider, AuthResource } from "./AuthContext";
import { useApi } from "../api/api";
import AsyncStorage from "@react-native-async-storage/async-storage";
import { Box, Spinner } from "@gluestack-ui/themed";

export const AuthTokenContext = createContext<{
  setToken: (token: string | null) => void;
}>({ setToken: () => {} });

export default function AuthProvider({
  children,
}: {
  children: React.ReactNode;
}) {
  const [loaded, setLoaded] = useState(false);
  const [token, setToken] = useState<string | null>(null);

  useEffect(() => {
    (async () => {
      const saved = await AsyncStorage.getItem("token");
      setToken(saved);
      setLoaded(true);
    })();
  }, []);

  const { data, isFetching } = useApi<AuthResource>(
    {
      url: "/auth/users/me/",
      options: {},
    },
    {
      meta: {
        authorization: `JWT ${token}`,
      },
      enabled: loaded && !!token,
      queryKey: ["auth"],
    }
  );

  if (!loaded || (token && isFetching)) {
    return (
      <Box
        flex={1}
        justifyContent="center"
        alignItems="center"
        bg="$backgroundDark950"
      >
        <Spinner size="large" color="$white" />
      </Box>
    );
  }

  return (
    <AuthTokenContext.Provider value={{ setToken }}>
      <ContextProvider value={data ?? null}>{children}</ContextProvider>
    </AuthTokenContext.Provider>
  );
}

export const useAuthToken = () => useContext(AuthTokenContext);
