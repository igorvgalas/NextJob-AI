import React, { useState } from "react";
import { Box, Text, VStack, Avatar, Divider, Pressable } from "@gluestack-ui/themed";
import { ScrollView, Dimensions } from "react-native";
import { useAuth } from "../context/AuthContext";
import AppLayout from "../layouts/AppLayout";
import { ChevronDown, ChevronRight } from "lucide-react-native";


const sections = [
  { title: "Account", content: "Account details and security settings." },
  { title: "Profile", content: "Edit your profile information." },
  { title: "Location", content: "Manage your location preferences." },
  { title: "Preferences", content: "Set your app preferences." },
  { title: "Notification Settings", content: "Configure your notifications." },
];

const AccountScreen: React.FC = () => {
  const user = useAuth();
  const [expanded, setExpanded] = useState<string | null>(null);

  return (
    <AppLayout>
      <ScrollView contentContainerStyle={{ flexGrow: 1 }}>
        <Box flex={1} bg="$backgroundDark950" px="$4" py="$6">
          <VStack alignItems="center" space="md" mt={32}>
            <Avatar size="2xl" bg="$backgroundDark900" borderColor="$blue500" borderWidth={2}>
              <Text color="$white" fontSize="$2xl" fontWeight="$bold">
                {user.first_name[0]?.toUpperCase() + user.last_name[0]?.toUpperCase()}
              </Text>
            </Avatar>
            <Text color="$white" fontSize="$lg" fontWeight="$bold">
              {user.first_name + " " + user.last_name}
            </Text>
            <Text color="$coolGray400" fontSize="$md">
              {user.email}
            </Text>
          </VStack>

          <Divider my="$6" />

          <VStack width="100%">
            {sections.map((section) => {
              const isExpanded = expanded === section.title;
              return (
                <Box
                  key={section.title}
                  width="100%"
                  borderWidth={1}
                  borderColor={isExpanded ? "$blue600" : "$backgroundDark700"}
                  borderRadius={12}
                  mb={3}
                  bg="$backgroundDark900"
                  overflow="hidden"
                  shadowColor={isExpanded ? "$blue600" : "$black"}
                  shadowOpacity={isExpanded ? 0.15 : 0.05}
                  shadowRadius={6}
                >
                  <Pressable
                    width="100%"
                    onPress={() => setExpanded(isExpanded ? null : section.title)}
                    flexDirection="row"
                    justifyContent="space-between"
                    alignItems="center"
                    py="$4"
                    px="$3"
                  >
                    <Text
                      color={isExpanded ? "$blue500" : "$white"}
                      fontWeight="$bold"
                      fontSize="$md"
                    >
                      {section.title}
                    </Text>
                    {isExpanded ? (
                      <ChevronDown color="#3b82f6" size={28} />
                    ) : (
                      <ChevronRight color="#3b82f6" size={28} />
                    )}
                  </Pressable>
                  {isExpanded && (
                    <Box px="$3" pb="$3">
                      <Text color="$coolGray300">{section.content}</Text>
                    </Box>
                  )}
                </Box>
              );
            })}
          </VStack>
        </Box>
      </ScrollView>
    </AppLayout>
  );
};

export default AccountScreen;