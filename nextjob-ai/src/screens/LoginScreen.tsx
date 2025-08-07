import React, { useEffect, useState } from "react";
import { Formik } from "formik";
import {
  VStack,
  Box,
  Text,
  Input,
  Image,
  InputField,
  InputSlot,
  InputIcon,
  Button,
  ButtonText,
  FormControl,
  EyeIcon,
  EyeOffIcon,
  Divider,
} from "@gluestack-ui/themed";
import { useLogin } from "../hooks/useLogin";
import { useNavigation } from "@react-navigation/native";
import AsyncStorage from "@react-native-async-storage/async-storage";
import { Alert } from "react-native";
import * as Google from "expo-auth-session/providers/google";
import Constants from "expo-constants";
import { useApiMutation } from "../api/api";
import { useAuthToken } from "../context/AuthProvider";
import { AntDesign } from "@expo/vector-icons";
import AuthLayout from "../layouts/AuthLayout";

interface GoogleAuthResponse {
  access: string;
  refresh: string;
  user: {
    pk: number;
    username: string;
    email: string;
    first_name: string;
    last_name: string;
  };
  created: boolean;
}

export default function LoginScreen() {
  const { setToken } = useAuthToken();
  const [showPassword, setShowPassword] = useState(false);
  const navigation = useNavigation();
  const login = useLogin();
  const iosClientId = Constants.expoConfig?.extra?.IOS_GOOGLE_CLIENT_ID;

  const [request, response, promptAsync] = Google.useAuthRequest(
    iosClientId
      ? {
          iosClientId,
          redirectUri: "ai.nextjob.client:/oauth2redirect/google",
          scopes: [
            "profile",
            "email",
            "https://www.googleapis.com/auth/gmail.readonly",
          ],
        }
      : {}
  );

  const handleTogglePassword = () => setShowPassword((prev) => !prev);

  const googleMutation = useApiMutation<
    { id_token: string; accessToken?: string },
    GoogleAuthResponse
  >(({ id_token, accessToken }) => ({
    url: "/auth/google-login",
    options: {
      method: "POST",
      body: { id_token, accessToken },
    },
  }));

  useEffect(() => {
    const handleGoogleResponse = async () => {
      if (response?.type !== "success") return;
      const authentication = response.authentication;
      const id_token = (authentication as { idToken?: string })?.idToken;
      const accessToken = authentication.accessToken;
      if (!id_token) return;

      try {
        const res = await googleMutation.mutateAsync({ id_token, accessToken });
        const { access, refresh, user, created } = res;
        console.log("Google login response:", res);

        // Save tokens and setToken BEFORE navigation
        await AsyncStorage.setItem("token", access);
        await AsyncStorage.setItem("refreshToken", refresh);
        setToken(access);
        // Delay navigation to ensure context updates
        setTimeout(() => {
          const missingProfile =
            created ||
            !user.first_name?.trim() ||
            !user.last_name?.trim() ||
            !user.username?.trim() ||
            user.email === user.username;

          if (missingProfile) {
            console.log("Redirecting to CompleteProfile");
            // @ts-expect-error
            navigation.navigate("CompleteProfile" as never, { user } as never);
          } else {
            console.log("Redirecting to Home");
            navigation.navigate("Home" as never);
          }
        }, 100);
        console.log("✅ Authenticated user:", user);
      } catch (error: any) {
        console.error("❌ Google login failed:", error);
        Alert.alert("Google login failed", error.message);
      }
    };

    handleGoogleResponse();
  }, [response]);

  return (
    <AuthLayout>
      <Image
        source={require("../../assets/logo.png")}
        alt="NextJob AI Logo"
        width={300}
        height={300}
        resizeMode="contain"
        alignSelf="center"
      />

      <Formik
        initialValues={{ username: "", password: "" }}
        onSubmit={(values) => {
          login(values);
        }}
      >
        {({ handleChange, handleSubmit, values }) => (
          <FormControl width="100%" px="$8">
            <VStack space="lg">
              <VStack space="xs">
                <Text color="$coolGray300">Email</Text>
                <Input borderColor="$coolGray600">
                  <InputField
                    type="text"
                    value={values.username}
                    onChangeText={handleChange("email")}
                    placeholder="Enter your email"
                    color="$white"
                    placeholderTextColor="$coolGray400"
                  />
                </Input>
              </VStack>

              <VStack space="xs">
                <Text color="$coolGray300">Password</Text>
                <Input borderColor="$coolGray600">
                  <InputField
                    type={showPassword ? "text" : "password"}
                    value={values.password}
                    onChangeText={handleChange("password")}
                    placeholder="Enter your password"
                    color="$white"
                    placeholderTextColor="$coolGray400"
                  />
                  <InputSlot pr="$3" onPress={handleTogglePassword}>
                    <InputIcon as={showPassword ? EyeIcon : EyeOffIcon} />
                  </InputSlot>
                </Input>
              </VStack>

              <Button
                bg="$blue600"
                borderRadius="$md"
                onPress={handleSubmit as any}
                isDisabled={!values.username || !values.password}
              >
                <ButtonText color="$white" fontWeight="$bold">
                  Log in
                </ButtonText>
              </Button>

              <Box flexDirection="row" alignItems="center" my="$2">
                <Divider flex={1} mx={2} />
                <Text color="$coolGray400" mx={2}>
                  or
                </Text>
                <Divider flex={1} mx={2} />
              </Box>

              <Button
                variant="outline"
                borderRadius="$md"
                flexDirection="row"
                alignItems="center"
                justifyContent="center"
                onPress={() => promptAsync()}
              >
                <AntDesign
                  name="google"
                  size={20}
                  color="#4285F4"
                  style={{ marginRight: 8 }}
                />
                <ButtonText color="$white" fontWeight="$bold">
                  Log in with Google
                </ButtonText>
              </Button>

              <Button
                variant="link"
                onPress={() => navigation.navigate("Register" as never)}
              >
                <ButtonText color="$coolGray400">
                  Don't have an account? Register
                </ButtonText>
              </Button>
            </VStack>
          </FormControl>
        )}
      </Formik>
    </AuthLayout>
  );
}
