import React from "react";
import {
  Box,
  Text,
  VStack,
  HStack,
  Button,
  Badge,
  Icon,
} from "@gluestack-ui/themed";
import { JobType } from "../types/JobType";
import { ArrowLeft, MapPin } from "lucide-react-native";
import { Pressable } from "react-native";
import { useNavigation, useRoute } from "@react-navigation/native";
import { Linking } from "react-native";

export default function JobDetailsScreen() {
  const navigation = useNavigation();
  const route = useRoute();
  const { job } = route.params as { job: JobType };

  return (
    <Box flex={1} bg="$black" px="$5" pt="$12">
      <Pressable onPress={() => navigation.goBack()}>
        <HStack alignItems="center" mt={4} mb="$4">
          <Icon as={ArrowLeft} size="lg" color="$white" />
          {/* <Text color="$white" fontSize="$md" ml="$2">
            Back
          </Text> */}
        </HStack>
      </Pressable>

      <VStack space="md">
        <HStack justifyContent="space-between" alignItems="center">
          <Text
            fontSize="$2xl"
            fontWeight="$bold"
            color="$white"
            flexShrink={1}
          >
            {job.title}
          </Text>
          <Badge bg="$blue600" borderRadius="$full" px="$3" py="$1">
            <Text color="$white" fontSize="$xs" fontWeight="$bold">
              Matching {Math.round(job.match_score * 10)}%
            </Text>
          </Badge>
        </HStack>

        <Text color="$coolGray300" fontSize="$md" fontWeight="$medium">
          {job.company}
        </Text>

        <HStack alignItems="center">
          <Icon as={MapPin} color="$coolGray400" size="sm" mr="$1" />
          <Text color="$coolGray400" fontSize="$sm">
            {job.location}
          </Text>
        </HStack>

        <Text color="$coolGray500" fontSize="$xs" mt="$2">
          Posted {new Date(job.created_at).toLocaleDateString()}
        </Text>

        <Box borderBottomWidth={1} borderColor="$coolGray800" my="$4" />
        <Text fontSize="$lg" color="$white" fontWeight="$bold">
          Job Analysis from AI
        </Text>
        <Text fontSize="$md" color="$coolGray300" lineHeight="$md">
          {job.reason}
        </Text>
        <Button
          bg="$blue600"
          mt="$8"
          borderRadius="$lg"
          onPress={() => Linking.openURL(job.apply_link)}
        >
          <Text color="$white" fontWeight="$bold" fontSize="$md">
            Apply Now
          </Text>
        </Button>
      </VStack>
    </Box>
  );
}
