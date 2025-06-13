import React, { useEffect } from "react";
import { ActivityIndicator } from "react-native";
import AsyncStorage from "@react-native-async-storage/async-storage";
import { useNavigation } from "@react-navigation/native";
import { Box, Text, Spinner, VStack, Image } from "@gluestack-ui/themed";

export default function LoadingScreen() {
  const navigation = useNavigation();

  useEffect(() => {
    (async () => {
      const token = await AsyncStorage.getItem("token");
      if (token) {
        // Optionally, set the token in your AuthProvider context here if needed
        navigation.reset({ index: 0, routes: [{ name: "Home" as never }] });
      } else {
        navigation.reset({ index: 0, routes: [{ name: "Login" as never }] });
      }
    })();
  }, []);

  return (
    <Box
      flex={1}
      bg="$backgroundDark950" // Or replace with a custom blue hex: "#007AFF"
      justifyContent="center"
      alignItems="center"
      px="$4"
    >
      <VStack space="xl" alignItems="center">
        <Image
          source={require("../../assets/logo.png")}
          alt="NextJob AI Logo"
          width={600}
          height={600}
          resizeMode="contain"
        />
        <Text fontSize="$xl" color="$white" fontWeight="$bold">
          Loading NextJob AI...
        </Text>
        <Spinner size="large" color="$white" />
      </VStack>
    </Box>
  );
}
