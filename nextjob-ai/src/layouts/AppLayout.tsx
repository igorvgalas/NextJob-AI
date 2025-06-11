import React from "react";
import { Box } from "@gluestack-ui/themed";
import NavBar from "../components/NavBar";
import BottomMenu from "../components/BottomMenu";

interface AppLayoutProps {
  children: React.ReactNode;
  onLogout: () => void;
}

const AppLayout: React.FC<AppLayoutProps> = ({ children, onLogout }) => (
  <Box flex={1} bg="$backgroundDark950">
    <NavBar onLogout={onLogout} />
    <Box flex={1} px="$4" pt="$4">
      {children}
    </Box>
    <BottomMenu />
  </Box>
);

export default AppLayout;
