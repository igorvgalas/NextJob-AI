import React from "react";
import { HStack, Text, Pressable } from "@gluestack-ui/themed";

interface NavBarProps {
  onLogout: () => void;
}

const NavBar: React.FC<NavBarProps> = ({ onLogout }) => {
  // Uncontrolled Menu: Gluestack handles open/close via triggerProps

  return (
    <HStack
      bg="$black"
      px="$4"
      pt="$12"
      pb="$4"
      alignItems="center"
      justifyContent="space-between"
    >
      <Text color="$white" fontSize="$xl" fontWeight="$bold">
        NextJob AI
      </Text>
      <HStack space="md">
        <Pressable accessibilityRole="button" onPress={onLogout}>
          <Text
            color="$white"
            fontWeight="$bold"
            fontSize="$md"
            px="$3"
            py="$2"
          >
            Logout
          </Text>
        </Pressable>
      </HStack>
    </HStack>
  );
};

export default NavBar;
