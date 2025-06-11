import React from "react";
import { Formik } from "formik";
import {
  VStack,
  Box,
  Text,
  Heading,
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
import { ArrowLeft, MapPin } from "lucide-react-native";
import { useApiMutation } from "../api/api";
import { useNavigation } from "@react-navigation/native";
import AsyncStorage from "@react-native-async-storage/async-storage";

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

  const handleLogout = async () => {
      await AsyncStorage.removeItem("token");
      await AsyncStorage.removeItem("refreshToken");
      navigation.navigate("Login" as never);
    };

  return (
    <>
    <Box bg="$blue800" px="$4" pt="$12">
        <Pressable onPress={() => navigation.goBack()}>
          <HStack alignItems="center" mb="$4">
            <Icon as={ArrowLeft} size="md" color="$white" />
            <Text color="$white" fontSize="$md" ml="$2">
              Back
            </Text>
          </HStack>
        </Pressable>
      </Box>
      <Box flex={1} bg="$blue800" justifyContent="center" px="$12">
        <Formik
          initialValues={{ username: "", email: "", password: "" }}
          onSubmit={handleSubmit}
        >
          {({ handleChange, handleSubmit, values }) => (
            <FormControl>
              <VStack space="xl">
                <Heading color="$white">Register</Heading>

                <VStack space="xs">
                  <Text color="$white">Username</Text>
                  <Input borderColor="$white">
                    <InputField
                      type="text"
                      value={values.username}
                      onChangeText={handleChange("username")}
                      placeholder="Enter your username"
                    />
                  </Input>
                </VStack>

                <VStack space="xs">
                  <Text color="$white">Email</Text>
                  <Input borderColor="$white">
                    <InputField
                      type="text"
                      value={values.email}
                      onChangeText={handleChange("email")}
                      placeholder="Enter your email"
                    />
                  </Input>
                </VStack>

                <VStack space="xs">
                  <Text color="$white">Password</Text>
                  <Input borderColor="$white">
                    <InputField
                      type={showPassword ? "text" : "password"}
                      value={values.password}
                      onChangeText={handleChange("password")}
                      placeholder="Enter your password"
                    />
                    <InputSlot onPress={handleTogglePassword}>
                      <InputIcon as={showPassword ? EyeIcon : EyeOffIcon} />
                    </InputSlot>
                  </Input>
                </VStack>

                <Button onPress={() => handleSubmit()}>
                  <ButtonText>Register</ButtonText>
                </Button>
                <Button variant="outline" onPress={handleLogout}>
                  <ButtonText>Logout</ButtonText>
                </Button>
              </VStack>
            </FormControl>
          )}
        </Formik>
      </Box>
    </>
  );
}
