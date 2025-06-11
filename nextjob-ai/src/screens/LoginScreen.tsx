import React, { useEffect } from "react";
import { Formik } from "formik";
import {
  VStack,
  Box,
  Text,
  Heading,
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
} from "@gluestack-ui/themed";
import { useLogin } from "../hooks/useLogin"; // або шлях до useLogin
import { useNavigation } from "@react-navigation/native";
import AsyncStorage from "@react-native-async-storage/async-storage";

export default function LoginScreen() {
  const [showPassword, setShowPassword] = React.useState(false);
  const handleTogglePassword = () => setShowPassword((prev) => !prev);
  const { mutate: login } = useLogin();
  const navigation = useNavigation();

  useEffect(() => {
    (async () => {
      const token = await AsyncStorage.getItem("token");
      if (token) {
        navigation.reset({
          index: 0,
          routes: [{ name: "Home" as never }],
        });
      }
    })();
  }, []);

  return (
    <Box flex={1} bg="$blue800" justifyContent="center" px="$12">
      <Formik
        initialValues={{ username: "", password: "" }}
        onSubmit={(values) => {
          login(values, {
            onSuccess: () => navigation.navigate("Home" as never),
          });
        }}
      >
        {({ handleChange, handleSubmit, values }) => (
          <FormControl>
            <VStack space="xl">
              <VStack space="xs">
                <Image
                  source={require("../../assets/logo.png")}
                  alt="NextJob AI Logo"
                  width={150}
                  height={150}
                  // resizeMode="contain"
                  alignSelf="center"
                />
                <Text className="text-typography-500">Email</Text>
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
                <Text className="text-typography-500">Password</Text>
                <Input borderColor="$white">
                  <InputField
                    type={showPassword ? "text" : "password"}
                    value={values.password}
                    onChangeText={handleChange("password")}
                    placeholder="Enter your password"
                  />
                  <InputSlot className="pr-3" onPress={handleTogglePassword}>
                    <InputIcon as={showPassword ? EyeIcon : EyeOffIcon} />
                  </InputSlot>
                </Input>
              </VStack>

              <Button onPress={() => handleSubmit()}>
                <ButtonText className="text-typography-0">Login</ButtonText>
              </Button>
              <Button
                variant="link"
                onPress={() => navigation.navigate("Register" as never)}
              >
                <ButtonText className="text-typography-500">
                  Don't have an account? Register
                </ButtonText>
              </Button>
            </VStack>
          </FormControl>
        )}
      </Formik>
    </Box>
  );
}
