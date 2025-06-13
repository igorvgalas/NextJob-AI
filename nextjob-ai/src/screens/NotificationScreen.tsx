import React from "react";
import { Box, Text } from "@gluestack-ui/themed";
import AppLayout from "../layouts/AppLayout";

export default function NotificationScreen() {
  return (
    <AppLayout>
      <Box
        flex={1}
        justifyContent="center"
        alignItems="center"
        bg="$backgroundDark950"
      >
        <Text color="$white" fontSize={24} fontWeight="$bold">
          Notifications
        </Text>
        <Text color="$coolGray400" mt={4}>
          This is the Notifications screen. Coming soon!
        </Text>
      </Box>
    </AppLayout>
  );
}
