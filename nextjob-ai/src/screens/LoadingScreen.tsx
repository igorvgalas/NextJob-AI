import React, { useEffect } from "react";
import { ActivityIndicator } from "react-native";
import AsyncStorage from "@react-native-async-storage/async-storage";
import { useNavigation } from "@react-navigation/native";
import { Box, Text, Spinner, VStack, Image } from "@gluestack-ui/themed";
import Loader from "../components/Loader";

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

  return <Loader />;
}
