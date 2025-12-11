import React, { useState } from "react";
import { HStack, Text, Pressable, Menu } from "@gluestack-ui/themed";

interface NavBarProps {
  onLogout: () => void;
}

const NavBar: React.FC<NavBarProps> = ({ onLogout }) => {
  const [menuOpen, setMenuOpen] = useState(false);

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
        <Menu
          isOpen={menuOpen}
          placement="bottom right"
          onClose={() => setMenuOpen(false)}
          backgroundColor="$black"
          borderColor="$gray500"
          borderWidth={1}
          borderRadius="$md"
          trigger={(triggerProps) => (
            <Pressable
              {...triggerProps}
              onPress={() => setMenuOpen((open) => !open)}
            >
              <Text
                color="$white"
                fontWeight="$bold"
                fontSize="$lg"
                alignContent="center"
                justifyContent="center"
              >
                . . .
              </Text>
            </Pressable>
          )}
        >
          <Menu.Backdrop />
          <Menu.Content
            backgroundColor="$black"
            borderColor="$gray500"
            borderWidth={1}
            borderRadius="$md"
            minWidth={150}
            paddingVertical="$2"
          >
            <Menu.Item
              key="logout"
              textValue="Logout"
              onPress={() => {
                setMenuOpen(false);
                onLogout();
              }}
            >
              <Menu.ItemLabel color="$white" fontWeight="$bold">
                Logout
              </Menu.ItemLabel>
            </Menu.Item>
          </Menu.Content>
        </Menu>
      </HStack>
    </HStack>
  );
};

export default NavBar;
