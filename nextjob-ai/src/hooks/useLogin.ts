import { useNavigation } from "@react-navigation/native";
import { useApiMutation } from "../api/api";
import AsyncStorage from "@react-native-async-storage/async-storage";

interface LoginCredentials {
  username: string;
  password: string;
}

interface LoginResponse {
  access: string;
  refresh: string;
}

export function useLogin() {
  const navigation = useNavigation();
  
  return useApiMutation<LoginCredentials, LoginResponse>(
    (creds) => ({
      url: "/auth/jwt/login",
      options: {
        method: "POST",
        body: new URLSearchParams({
          username: creds.username,
          password: creds.password,
        }).toString(),
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
      },
    }),
    {
      onSuccess: async (data) => {
        await AsyncStorage.setItem("token", data.access);
        await AsyncStorage.setItem("refreshToken", data.refresh);
        navigation.navigate("Home" as never);
      },
    },
    ["auth"]
  );
}