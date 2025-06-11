import React from "react";
import { Linking } from "react-native";
import {
  Box,
  Text,
  VStack,
  HStack,
  Pressable,
  Badge,
} from "@gluestack-ui/themed";
import { JobType } from "../types/JobType";
import { formatDistanceToNow } from "date-fns";
import { useNavigation } from "@react-navigation/native";

export default function JobCard({ job }: { job: JobType }) {
  const navigation = useNavigation();

  return (
    <Pressable onPress={() => navigation.navigate("JobDetails", { job })}>
      <Box
        bg="$black"
        borderRadius="$xl"
        p="$5"
        mb="$5"
        shadowColor="$black"
        shadowOffset={{ width: 0, height: 2 }}
        shadowOpacity={0.2}
        shadowRadius={6}
      >
        <VStack space="md">
          <HStack justifyContent="space-between" alignItems="center">
            <Text
              fontSize="$lg"
              fontWeight="$bold"
              color="$white"
              flexShrink={1}
            >
              {job.title}
            </Text>
            <Badge
              action="success"
              bg="$blue600"
              borderRadius="$full"
              px="$3"
              py="$1"
            >
              <Text color="$white" fontSize="$xs" fontWeight="$bold">
                Matching {Math.round(job.match_score * 10)}%
              </Text>
            </Badge>
          </HStack>

          <Text fontSize="$sm" color="$coolGray300">
            {job.company} • {job.location}
          </Text>

          <Text fontSize="$xs" color="$coolGray500">
            {formatDistanceToNow(new Date(job.created_at), { addSuffix: true })}
          </Text>
        </VStack>
      </Box>
    </Pressable>
  );
}
