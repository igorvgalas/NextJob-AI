import React from "react";
import { Box } from "@gluestack-ui/themed";
import NavBar from "../components/NavBar";
import BottomMenu from "../components/BottomMenu";
import { useAuthToken } from "../context/AuthProvider";
import AsyncStorage from "@react-native-async-storage/async-storage";// Adjust the import based on your project structure
import { useNavigation } from "@react-navigation/native";

interface AppLayoutProps {
  children: React.ReactNode;
}

const AppLayout: React.FC<AppLayoutProps> = ({ children }) => {
  const { setToken } = useAuthToken();
  const navigation = useNavigation();
  const handleLogout = async () => {
    await AsyncStorage.removeItem("token");
    await AsyncStorage.removeItem("refreshToken");
    setToken(null);
    navigation.navigate("Login" as never);
  };

  return (
    <Box flex={1} bg="$backgroundDark950">
      <NavBar onLogout={handleLogout} />
      <Box flex={1} px="$4" pt="$4">
        {children}
      </Box>
      <BottomMenu />
    </Box>
  );
};

export default AppLayout;
