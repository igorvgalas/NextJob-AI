import React from "react";
import { Box } from "@gluestack-ui/themed";
import { useAuthToken } from "../context/AuthProvider";
import AsyncStorage from "@react-native-async-storage/async-storage";
import { useNavigation } from "@react-navigation/native";
import { KeyboardAvoidingView, Platform, ScrollView } from "react-native";

interface AuthLayoutProps {
  children: React.ReactNode;
}

const AuthLayout: React.FC<AuthLayoutProps> = ({ children }) => {
  const { setToken } = useAuthToken();
  const navigation = useNavigation();
  const handleLogout = async () => {
    await AsyncStorage.removeItem("token");
    await AsyncStorage.removeItem("refreshToken");
    setToken(null);
    navigation.navigate("Login" as never);
  };

  return (
    <KeyboardAvoidingView
      style={{ flex: 1, backgroundColor: "#18181b" }}
      behavior={Platform.OS === "ios" ? "padding" : "height"}
    >
      <ScrollView
        contentContainerStyle={{ flexGrow: 1 }}
        keyboardShouldPersistTaps="handled"
        style={{ backgroundColor: "transparent" }}
      >
        <Box flex={1} bg="$backgroundDark950" width="100%">
          <Box pt="$12" width="100%">
            {children}
          </Box>
        </Box>
      </ScrollView>
    </KeyboardAvoidingView>
  );
};

export default AuthLayout;
