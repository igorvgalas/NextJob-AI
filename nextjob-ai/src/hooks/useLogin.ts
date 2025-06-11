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
      url: "/auth/jwt/create/",
      options: {
        method: "POST",
        body: creds,
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