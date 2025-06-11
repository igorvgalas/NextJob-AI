import React from "react";
import { Box, Text, Spinner, VStack, Image } from "@gluestack-ui/themed";

export default function LoadingScreen() {
  return (
    <Box
      flex={1}
      bg="$blue800" // Or replace with a custom blue hex: "#007AFF"
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
