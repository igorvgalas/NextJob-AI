import React from "react";
import { VStack, Button, ButtonText } from "@gluestack-ui/themed";
import AppLayout from "../layouts/AppLayout";
import { useApi, useApiMutation } from "../api/api";
import { Formik } from "formik";
import SectionedMultiSelect from "react-native-sectioned-multi-select";
import Icon from "react-native-vector-icons/MaterialIcons";

type Skills = {
  id: string;
  name: string;
};

export default function SkillsScreen() {
  const { data: skills, isLoading } = useApi<Skills[]>(
    {
      url: "/api/skills/",
      options: {},
    },
    {
      meta: {
        headers: {
          "Content-Type": "application/json",
        },
      },
      queryKey: ["skills"],
    }
  );
  console.log("Skills:", skills);

  const mutation = useApiMutation<any, any>((data) => ({
    url: "api/userskills/",
    options: {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: data,
    },
  }));

  return (
    <AppLayout>
        <Formik
          initialValues={{ skills: [] }}
          onSubmit={(values) => {
            console.log("Submitted:", values.skills);
            mutation.mutate({ skills: values.skills });
          }}
        >
          {({ values, setFieldValue, handleSubmit }) => (
            <VStack space="md" padding={4} width="100%">
              <SectionedMultiSelect
                items={skills?.map((s) => ({ id: s.id, name: s.name })) || []}
                uniqueKey="id"
                selectText="Select your skills"
                onSelectedItemsChange={(selected) =>
                  setFieldValue("skills", selected)
                }
                selectedItems={values.skills}
                searchPlaceholderText="Search skills..."
                IconRenderer={Icon}
                showDropDowns={true}
                styles={{
                  selectToggle: {
                    backgroundColor: "black",
                    borderColor: "#4b5563",
                    borderWidth: 1,
                    padding: 12,
                    borderRadius: 10,
                  },
                  selectToggleText: {
                    color: "#f9fafb",
                    fontSize: 16,
                  },
                  itemText: {
                    color: "black",
                  },
                  selectedItemText: {
                    color: "#10b981",
                  },
                  confirmText: {
                    color: "white",
                  },
                }}
              />
              <Button bgColor="$blue600" onPress={() => handleSubmit()}>
                <ButtonText>Submit Skills</ButtonText>
              </Button>
              <Button bgColor="$blue600" onPress={() => setFieldValue("skills", [])}>
                <ButtonText>Clear Skills</ButtonText>
              </Button>
            </VStack>
          )}
        </Formik>
    </AppLayout>
  );
}
