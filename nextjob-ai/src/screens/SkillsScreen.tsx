import React from "react";
import { VStack, Button, ButtonText } from "@gluestack-ui/themed";
import AppLayout from "../layouts/AppLayout";
import { useApi, useApiMutation } from "../api/api";
import { Formik } from "formik";
import SectionedMultiSelect from "react-native-sectioned-multi-select";
import Icon from "react-native-vector-icons/MaterialIcons";
import { useAuth } from "../context/AuthContext";

type Skills = {
  id: number;
  name: string;
};

type UserSkills = {
  id: number;
  user_id: number;
  skills: Skills[];
};

type FormValues = {
  skills: number[];
};

type UserSkillsPayload = {
  skill_ids: number[];
};

export default function SkillsScreen() {
  const user = useAuth();
  const { data: userSkills, isLoading: userSkillsLoading } = useApi<UserSkills>(
    {
      url: `/user_skills/user/${user.id}`,
      options: {},
    },
    {
      queryKey: ["userSkills"],
    }
  );
  // Defensive: ensure userSkills is always an array
  const safeUserSkills = Array.isArray(userSkills.skills) ? userSkills.skills : [];
  console.log("Safe User Skills:", safeUserSkills);
  const userSkillId = userSkills?.id;
  console.log("User Skill ID:", userSkillId);
  const initialSkillIds =
    userSkills?.skills?.map((skill) => skill.id) || [];

  const { data: skills, isLoading } = useApi<Skills[]>(
    {
      url: "/skills",
      options: {},
    },
    {
      queryKey: ["userSkills", user.id],
    }
  );
  const createMutation = useApiMutation<
    UserSkillsPayload & { user_id: number },
    any
  >(
    (data) => ({
      url: `/user_skills`,
      options: {
        method: "POST",
        body: data,
      },
    }),
    undefined,
    ["userSkills", user.id]
  );

  const mutation = useApiMutation<UserSkillsPayload, any>(
    (data) => ({
      url: `/user_skills/${userSkillId}`,
      options: {
        method: "PATCH",
        body: data,
      },
    }),
    undefined,
    ["userSkills", user.id]
  );

  return (
    <AppLayout>
      <Formik<FormValues>
        enableReinitialize={true}
        initialValues={{ skills: initialSkillIds }}
        onSubmit={(values) => {
          const skillIds = values.skills;
          if (userSkillId) {
            mutation.mutate({ skill_ids: skillIds });
          } else {
            createMutation.mutate({ user_id: user.id, skill_ids: skillIds });
          }
        }}
      >
        {({ values, setFieldValue, handleSubmit, dirty }) => (
          <VStack space="md" padding={4} width="100%">
            <SectionedMultiSelect
              items={skills?.map((s) => ({ id: s.id, name: s.name })) || []}
              uniqueKey="id"
              selectText="Select your skills"
              onSelectedItemsChange={(selected) =>
                setFieldValue("skills", selected)
              }
              selectedItems={values.skills}
              // selectedItems={initialSkillIds}
              searchPlaceholderText="Search skills..."
              searchIconComponent={
                <Icon name="search" size={20} color="#ffffff" /> // White color icon
              }
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
                item: {
                  backgroundColor: "#1f2937",
                },
                itemText: {
                  color: "white",
                },
                selectedItemText: {
                  color: "#10b981",
                },
                confirmText: {
                  color: "white",
                },
                container: {
                  backgroundColor: "#1f2937",
                },
                searchBar: {
                  backgroundColor: "#374151",
                },
                separator: {
                  backgroundColor: "#1f2937",
                },
              }}
            />

            <Button
              bgColor="$blue600"
              onPress={() => handleSubmit()}
              isDisabled={!dirty}
            >
              <ButtonText>Submit Skills</ButtonText>
            </Button>
            <Button
              bgColor="$blue600"
              onPress={() => setFieldValue("skills", [])}
            >
              <ButtonText>Clear Skills</ButtonText>
            </Button>
          </VStack>
        )}
      </Formik>
    </AppLayout>
  );
}
