import React, { useEffect, useState } from "react";
import { ContextProvider, AuthResource } from "./AuthContext";
import { useApi } from "../api/api";
import AsyncStorage from "@react-native-async-storage/async-storage";
import { Box, Text } from "@gluestack-ui/themed";

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
        <Text color="$textLight900">Loading...</Text>
      </Box>
    );
  }

  return <ContextProvider value={data ?? null}>{children}</ContextProvider>;
}
