import React from "react";
import { Formik } from "formik";
import {
  VStack,
  Box,
  Text,
  Heading,
  Image,
  Input,
  InputField,
  InputSlot,
  InputIcon,
  Button,
  ButtonText,
  FormControl,
  EyeIcon,
  EyeOffIcon,
  Pressable,
  Icon,
  HStack,
} from "@gluestack-ui/themed";
import {
  Alert,
  KeyboardAvoidingView,
  Platform,
  ScrollView,
} from "react-native";
import { ArrowLeft, MapPin } from "lucide-react-native";
import { useApiMutation } from "../api/api";
import { useNavigation } from "@react-navigation/native";
import AsyncStorage from "@react-native-async-storage/async-storage";
import AppLayout from "../layouts/AppLayout";
import AuthLayout from "../layouts/AuthLayout";

interface RegisterCredentials {
  username: string;
  email: string;
  password: string;
}

interface RegisterResponse {
  id: number;
  username: string;
  email: string;
}

export default function RegisterScreen() {
  const [showPassword, setShowPassword] = React.useState(false);
  const handleTogglePassword = () => setShowPassword((prev) => !prev);
  const navigation = useNavigation();
  const { mutate: register } = useApiMutation<
    RegisterCredentials,
    RegisterResponse
  >(
    (creds) => ({
      url: "/auth/users/",
      options: {
        method: "POST",
        body: creds,
      },
    }),
    {
      onSuccess: (data) => {
        console.log("✅ Registration successful:", data);
        alert("Account created! You can now log in.");
      },
      onError: (error: any) => {
        console.error("❌ Registration error:", error);
        alert("Registration failed. Please check your details.");
      },
    }
  );

  // Handle form submission
  const handleSubmit = (values: RegisterCredentials) => {
    const response = register(values);
  };

  return (
    <AuthLayout>
        <KeyboardAvoidingView
          style={{ flex: 1, backgroundColor: "#18181b" }}
          behavior={Platform.OS === "ios" ? "padding" : "height"}
        >
          <ScrollView
            contentContainerStyle={{
              flexGrow: 1,
              justifyContent: "center",
              alignItems: "center",
            }}
            keyboardShouldPersistTaps="handled"
            style={{ backgroundColor: "transparent" }}
          >
            <Box
              pt="$12"
              px="$4"
              flex={1}
              justifyContent="flex-start"
              bg="$backgroundDark950"
              borderRadius="$lg"
              shadowColor="$black"
              shadowOffset={{ width: 0, height: 2 }}
              shadowOpacity={0.15}
              shadowRadius={8}
              width="100%"
              minHeight="100%"
            >
              <Pressable onPress={() => navigation.goBack()}>
                <HStack alignItems="center">
                  <Icon as={ArrowLeft} size="md" color="$white" />
                  <Text color="$white" ml="$2">
                    Back
                  </Text>
                </HStack>
              </Pressable>
              <Image
                source={require("../../assets/logo.png")}
                alt="NextJob AI Logo"
                width={300}
                height={300}
                resizeMode="contain"
                alignSelf="center"
              />
              <Formik
                initialValues={{ username: "", email: "", password: "" }}
                onSubmit={handleSubmit}
              >
                {({ handleChange, handleSubmit, values }) => (
                  <FormControl width="100%" px="$8">
                    <VStack space="xl">
                      <VStack space="xs">
                        <Text color="$white">Username</Text>
                        <Input borderColor="$coolGray600">
                          <InputField
                            type="text"
                            value={values.username}
                            onChangeText={handleChange("username")}
                            placeholder="Enter your username"
                            color="$white"
                            placeholderTextColor="$coolGray400"
                          />
                        </Input>
                      </VStack>

                      <VStack space="xs">
                        <Text color="$white">Email</Text>
                        <Input borderColor="$coolGray600">
                          <InputField
                            type="text"
                            value={values.email}
                            onChangeText={handleChange("email")}
                            placeholder="Enter your email"
                            color="$white"
                            placeholderTextColor="$coolGray400"
                          />
                        </Input>
                      </VStack>

                      <VStack space="xs">
                        <Text color="$white">Password</Text>
                        <Input borderColor="$coolGray600">
                          <InputField
                            type={showPassword ? "text" : "password"}
                            value={values.password}
                            onChangeText={handleChange("password")}
                            placeholder="Enter your password"
                            color="$white"
                            placeholderTextColor="$coolGray400"
                          />
                          <InputSlot onPress={handleTogglePassword}>
                            <InputIcon
                              as={showPassword ? EyeIcon : EyeOffIcon}
                            />
                          </InputSlot>
                        </Input>
                      </VStack>

                      <Button onPress={() => handleSubmit()}>
                        <ButtonText>Register</ButtonText>
                      </Button>
                    </VStack>
                  </FormControl>
                )}
              </Formik>
            </Box>
          </ScrollView>
        </KeyboardAvoidingView>
    </AuthLayout>
  );
}
