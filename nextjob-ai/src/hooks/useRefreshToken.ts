import AsyncStorage from '@react-native-async-storage/async-storage';
import Constants from 'expo-constants';

export async function refreshToken(): Promise<string | null> {
  const refresh = await AsyncStorage.getItem("refreshToken");

  if (!refresh) return null;

  const response = await fetch(`${Constants.expoConfig.extra.BASE_URL}/auth/jwt/refresh/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ refresh }),
  });

  if (!response.ok) {
    await AsyncStorage.multiRemove(["token", "refreshToken"]);
    return null;
  }

  const data = await response.json();
  await AsyncStorage.setItem("token", data.access);
  return data.access;
}