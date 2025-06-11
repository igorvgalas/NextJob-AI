import React from "react";
import { HStack, Pressable, Text, Icon } from "@gluestack-ui/themed";
import { Home, User, Bell, Star } from "lucide-react-native";
import { useNavigation, useRoute } from "@react-navigation/native";

const tabs = [
  { name: "Home", icon: Home },
  { name: "Skills", icon: Star },
  { name: "Notification", icon: Bell },
  { name: "Account", icon: User },
];

const BottomMenu: React.FC = () => {
  const navigation = useNavigation();
  const route = useRoute();

  return (
    <HStack
      bg="$black"
      px="$2"
      pb="$8"
      pt="$4"
      alignItems="center"
      justifyContent="space-around"
    >
      {tabs.map((tab) => {
        const isActive = route.name === tab.name;
        return (
          <Pressable
            key={tab.name}
            onPress={() => navigation.navigate(tab.name as never)}
            flex={1}
            alignItems="center"
          >
            <Icon
              as={tab.icon}
              color={isActive ? "$white" : "$blue500"}
              size="lg"
            />
            <Text mt="$2" color={"$white"} fontSize="$xs">
              {tab.name}
            </Text>
          </Pressable>
        );
      })}
    </HStack>
  );
};

export default BottomMenu;
