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
import LoadingScreen from "./src/screens/LoadingScreen";
import SkillsScreen from "./src/screens/SkillsScreen";
import NotificationScreen from "./src/screens/NotificationScreen";
import { GestureHandlerRootView } from "react-native-gesture-handler";
import AsyncStorage from "@react-native-async-storage/async-storage";

global.AsyncStorage = AsyncStorage;

// Uncomment the following lines to debug AsyncStorage contents
// This will log all keys and their values in AsyncStorage to the console
// Note: This can be useful for debugging but should be removed in production code.

// AsyncStorage.getAllKeys().then(keys => {
//   AsyncStorage.multiGet(keys).then(data => {
//     console.log("AsyncStorage contents:", data);
//   });
// });

const Stack = createNativeStackNavigator();

export const queryClient = new QueryClient();


export default function App() {
  const colorMode = useColorScheme();

  return (
    <GestureHandlerRootView style={{ flex: 1 }}>
      <QueryClientProvider client={queryClient}>
        <GluestackUIProvider mode={colorMode}>
          <AuthProvider>
            <NavigationContainer>
              <Stack.Navigator
                id={undefined}
                initialRouteName="Loading"
                screenOptions={{ headerShown: false }}
              >
                <Stack.Screen name="Loading" component={LoadingScreen} />
                <Stack.Screen name="Login" component={LoginScreen} />
                <Stack.Screen name="Home" component={HomeScreen} />
                <Stack.Screen name="JobDetails" component={JobDetailsScreen} />
                <Stack.Screen name="Register" component={RegisterScreen} />
                <Stack.Screen name="Account" component={AccountScreen} />
                <Stack.Screen name="Skills" component={SkillsScreen} />
                <Stack.Screen
                  name="Notification"
                  component={NotificationScreen}
                />
                <Stack.Screen
                  name="CompleteProfile"
                  component={CompleteProfileScreen}
                />
              </Stack.Navigator>
            </NavigationContainer>
          </AuthProvider>
        </GluestackUIProvider>
      </QueryClientProvider>
    </GestureHandlerRootView>
  );
}
