import React from "react";
import { Formik } from "formik";
import {
  VStack,
  Text,
  Input,
  InputField,
  Button,
  ButtonText,
  FormControl,
} from "@gluestack-ui/themed";
import { Alert } from "react-native";
import { useApiMutation } from "../api/api";
import AuthLayout from "../layouts/AuthLayout";
import AsyncStorage from "@react-native-async-storage/async-storage";

export default function CompleteProfileScreen({ navigation, route }) {
  const { user } = route.params || {};
  const token = AsyncStorage.getItem("token");
  const updateProfile = useApiMutation<any, any>((values) => ({
    url: `/auth/users/me/`,
    options: {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
        Authorization: `JWT ${token}`,
      },
      body: values,
    },
  }));

  return (
    <AuthLayout>
      <Text
        color="$white"
        fontSize={24}
        pt={24}
        mb={4}
        fontWeight="$bold"
        textAlign="center"
      >
        Complete Your Profile
      </Text>
      <Text color="$coolGray400" fontSize={16} textAlign="center" mb={8}>
        Please fill in your details to complete your profile.
      </Text>

      <Formik
        initialValues={{
          username: user?.username || "",
          first_name: user?.first_name || "",
          last_name: user?.last_name || "",
          password: "",
        }}
        onSubmit={async (values) => {
          try {
            await updateProfile.mutateAsync(values);
            Alert.alert("Profile updated!", "You can now use your account.");
            navigation.reset({ index: 0, routes: [{ name: "Home" }] });
          } catch (error: any) {
            Alert.alert("Update failed", error?.message || "Try again");
          }
        }}
      >
        {({ handleChange, handleSubmit, values }) => (
          <FormControl width="100%" px="$8" pt="$8">
            <VStack space="lg">
              <VStack space="xs">
                <Text color="$coolGray300">Username</Text>
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
                <Text color="$coolGray300">First Name</Text>
                <Input borderColor="$coolGray600">
                  <InputField
                    type="text"
                    value={values.first_name}
                    onChangeText={handleChange("first_name")}
                    placeholder="Enter your first name"
                    color="$white"
                    placeholderTextColor="$coolGray400"
                  />
                </Input>
              </VStack>
              <VStack space="xs">
                <Text color="$coolGray300">Last Name</Text>
                <Input borderColor="$coolGray600">
                  <InputField
                    type="text"
                    value={values.last_name}
                    onChangeText={handleChange("last_name")}
                    placeholder="Enter your last name"
                    color="$white"
                    placeholderTextColor="$coolGray400"
                  />
                </Input>
              </VStack>
              <VStack space="xs">
                <Text color="$coolGray300">Password</Text>
                <Input borderColor="$coolGray600">
                  <InputField
                    type="password"
                    value={values.password}
                    onChangeText={handleChange("password")}
                    placeholder="Set a password"
                    color="$white"
                    placeholderTextColor="$coolGray400"
                  />
                </Input>
              </VStack>
              <Button
                bg="$blue600"
                borderRadius="$md"
                onPress={handleSubmit as any}
                isDisabled={
                  !values.username ||
                  !values.first_name ||
                  !values.last_name ||
                  !values.password
                }
              >
                <ButtonText color="$white" fontWeight="$bold">
                  Save Profile
                </ButtonText>
              </Button>
            </VStack>
          </FormControl>
        )}
      </Formik>
    </AuthLayout>
  );
}
