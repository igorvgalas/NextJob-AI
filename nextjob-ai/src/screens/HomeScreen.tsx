import React, { useState, useRef, useEffect } from "react";
import { FlatList } from "react-native";
import { Box, Text, Pressable } from "@gluestack-ui/themed";
import Swipeable from "react-native-gesture-handler/Swipeable";
import { TrashIcon } from "lucide-react-native";
import JobCard from "../components/JobCard";
import AppLayout from "../layouts/AppLayout";
import { useAuth } from "../context/AuthContext";
import { queryApi, useApiMutation } from "../api/api";
import { useNavigation } from "@react-navigation/native";

export default function HomeScreen() {
  const user = useAuth();
  const navigation = useNavigation<any>();
  const [jobs, setJobs] = useState<any[]>([]);
  const [nextUrl, setNextUrl] = useState<string | null>("/api/jobs/?page=1");
  const [loadingMore, setLoadingMore] = useState(false);
  const [initialLoading, setInitialLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const isMounted = useRef(false);
  console.log("User:", user);

  useEffect(() => {
    if (!user) {
      navigation.reset({
        index: 0,
        routes: [{ name: "Login" }],
      });
    } else if (!user.username || user.username.trim() === "") {
      navigation.reset({
        index: 0,
        routes: [{ name: "CompleteProfile", params: { user } }],
      });
    }
  }, [user]);

  const mutation = useApiMutation<any, any>(
    (jobId: number) => ({
      url: `/job-offers/${jobId}`,
      options: {
        method: "DELETE",
      },
    }),
    undefined,
    ["jobs", user?.id]
  );

  // Fetch jobs page
  const fetchJobs = async (url: string, replace = false) => {
    setLoadingMore(true);
    setError(null);
    try {
      const data = await queryApi<any>(
        {
          url,
          options: { method: "GET" },
        },
        new Headers()
      );
      if (replace) {
        setJobs(data.results);
      } else {
        setJobs((prev) => [...prev, ...data.results]);
      }
      setNextUrl(
        data.next ? data.next.replace(/^http(s)?:\/\/[^/]+/, "") : null
      );
    } catch (e: any) {
      setError(e.message || "Unknown error");
    } finally {
      setLoadingMore(false);
      setInitialLoading(false);
    }
  };

  // Initial load
  React.useEffect(() => {
    if (!isMounted.current && user) {
      fetchJobs(`/job-offers/?page=1&user=${user.id}`, true);
      isMounted.current = true;
    }
  }, [user]);

  const handleEndReached = () => {
    if (nextUrl && !loadingMore) {
      fetchJobs(nextUrl);
    }
  };

  const handleDeleteUI = (jobId: number) => {
    mutation.mutate(jobId, {
      onSuccess: () => {
        setJobs((prev) => prev.filter((job) => job.id !== jobId));
        fetchJobs(`/job-offers/?page=1&user=${user.id}`, true);
      },
      onError: (error) => {
        console.error("Error deleting job:", error);
      },
    });
  };

  if (initialLoading) {
    return (
      <Box
        flex={1}
        justifyContent="center"
        alignItems="center"
        bg="$backgroundDark950"
      >
        <Text color="$textLight900">Loading jobs...</Text>
      </Box>
    );
  }

  if (error) {
    return (
      <AppLayout>
        <Box px="$4" pt="$6" pb="$2" bg="$backgroundDark950">
          <Box
            bg="$blue800"
            borderRadius={16}
            px="$4"
            py="$4"
            mb="$4"
            alignItems="center"
          >
            <Text color="$white" fontSize="$lg" fontWeight="$bold">
              Welcome, {user.username}!
            </Text>
            <Text color="$coolGray200" fontSize="$md" mt={2} textAlign="center">
              Discover your next opportunity. Browse the latest job offers
              below.
            </Text>
          </Box>
        </Box>
        <Box flex={1} justifyContent="center" alignItems="center">
          <Text color="$red600" fontSize="$lg">
            {error}
          </Text>
          <Pressable
            onPress={() =>
              fetchJobs(`/job-offers/?page=1&user=${user.id}`, true)
            }
          >
            <Text color="$blue600" fontSize="$md" mt={2}>
              Retry
            </Text>
          </Pressable>
        </Box>
      </AppLayout>
    );
  }

  return (
    <AppLayout>
      <Box px="$4" pt="$6" pb="$2" bg="$backgroundDark950">
        <Box
          bg="$blue800"
          borderRadius={16}
          px="$4"
          py="$4"
          mb="$4"
          alignItems="center"
        >
          <Text color="$white" fontSize="$lg" fontWeight="$bold">
            Welcome, {user.username}!
          </Text>
          <Text color="$coolGray200" fontSize="$md" mt={2} textAlign="center">
            Discover your next opportunity. Browse the latest job offers below.
          </Text>
        </Box>
      </Box>
      <FlatList
        data={jobs}
        keyExtractor={(item) => item.id.toString()}
        showsVerticalScrollIndicator={false}
        renderItem={({ item }) => (
          <Swipeable
            renderRightActions={() => (
              <Box
                mt={2}
                justifyContent="center"
                alignItems="center"
                width={80}
                bg="$red600"
                height="85%"
                borderRadius={8}
              >
                <Pressable onPress={() => handleDeleteUI(item.id)}>
                  <TrashIcon color="white" size={28} />
                </Pressable>
              </Box>
            )}
          >
            <JobCard job={item} />
          </Swipeable>
        )}
        onEndReached={handleEndReached}
        onEndReachedThreshold={0.5}
        ListFooterComponent={
          loadingMore ? (
            <Box py={4} alignItems="center">
              <Text color="$blue500">Loading more jobs...</Text>
            </Box>
          ) : null
        }
      />
    </AppLayout>
  );
}
