
import { useNavigation } from "@react-navigation/native";
import AsyncStorage from "@react-native-async-storage/async-storage";
import Constants from 'expo-constants';

interface LoginCredentials {
  email: string;
  password: string;
}

interface LoginResponse {
  access: string;
  refresh: string;
}

export function useLogin() {
  const navigation = useNavigation();
  const fetchurl = Constants.expoConfig.extra.BASE_URL;

  const login = async (creds: LoginCredentials) => {
    try {
      const response = await fetch(`${fetchurl}/auth/jwt/login`, {
        method: "POST",
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
        body: new URLSearchParams({
          email: creds.email,
          password: creds.password,
        }).toString(),
      });
      if (!response.ok) {
        throw new Error("Login failed");
      }
      const data: LoginResponse = await response.json();
      await AsyncStorage.setItem("token", data.access);
      await AsyncStorage.setItem("refreshToken", data.refresh);
      navigation.navigate("Home" as never);
      return data;
    } catch (error) {
      console.error("Login error:", error);
      throw error;
    }
  };

  return login;
}