import React from "react";
import { Box, ScrollView } from "@gluestack-ui/themed";
import NavBar from "../components/NavBar";
import BottomMenu from "../components/BottomMenu";
import { useAuthToken } from "../context/AuthProvider";
import AsyncStorage from "@react-native-async-storage/async-storage"; // Adjust the import based on your project structure
import { useNavigation, useRoute } from "@react-navigation/native";

interface AppLayoutProps {
  children: React.ReactNode;
}

const AppLayout: React.FC<AppLayoutProps> = ({ children }) => {
  const { setToken } = useAuthToken();
  const navigation = useNavigation();
  const route = useRoute();
  const handleLogout = async () => {
    await AsyncStorage.removeItem("token");
    await AsyncStorage.removeItem("refreshToken");
    setToken(null);
    navigation.navigate("Login" as never);
  };

  const isHomeScreen = route.name === "Home";

  return (
    <Box flex={1} bg="$backgroundDark950">
      <NavBar onLogout={handleLogout} />
      {isHomeScreen ? (
        <Box flex={1} px="$4" pt="$4">
          {children}
        </Box>
      ) : (
        <ScrollView
          contentContainerStyle={{ flexGrow: 1 }}
          keyboardShouldPersistTaps="handled"
          style={{ backgroundColor: "transparent" }}
        >
          <Box flex={1} px="$4" pt="$4">
            {children}
          </Box>
        </ScrollView>
      )}
      <BottomMenu />
    </Box>
  );
};

export default AppLayout;
