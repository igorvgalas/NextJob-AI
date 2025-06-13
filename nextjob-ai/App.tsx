import "@/global.css";
import { GluestackUIProvider } from "@/components/ui/gluestack-ui-provider";
import { QueryClientProvider, QueryClient } from "@tanstack/react-query";
import { NavigationContainer } from "@react-navigation/native";
import { createNativeStackNavigator } from "@react-navigation/native-stack";
import { useColorScheme } from "react-native";
import HomeScreen from "./src/screens/HomeScreen";
import JobDetailsScreen from "./src/screens/JobDetailsScreen";
import AuthProvider from "./src/context/AuthProvider";
import LoginScreen from "./src/screens/LoginScreen";
import RegisterScreen from "./src/screens/RegisterScreen";
import AccountScreen from "./src/screens/AccountScreen";
import CompleteProfileScreen from "./src/screens/CompleteProfileScreen";

const Stack = createNativeStackNavigator();

export const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: (count, error: any) => {
        // Only retry once on 401, but do not attempt async refresh here
        if (error?.status === 401 && count === 1) {
          return true;
        }
        return false;
      },
    },
  },
});

export default function App() {
  const colorMode = useColorScheme();

  return (
    <QueryClientProvider client={queryClient}>
      <GluestackUIProvider mode={colorMode}>
        <AuthProvider>
          <NavigationContainer>
            <Stack.Navigator
              id={undefined}
              screenOptions={{ headerShown: false }}
            >
              <Stack.Screen name="Login" component={LoginScreen} />
              <Stack.Screen name="Home" component={HomeScreen} />
              <Stack.Screen name="JobDetails" component={JobDetailsScreen} />
              <Stack.Screen name="Register" component={RegisterScreen} />
              <Stack.Screen name="Account" component={AccountScreen} />
              <Stack.Screen name="CompleteProfile" component={CompleteProfileScreen} />
            </Stack.Navigator>
          </NavigationContainer>
        </AuthProvider>
      </GluestackUIProvider>
    </QueryClientProvider>
  );
}
