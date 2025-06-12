import React, { useState, useRef } from "react";
import { FlatList } from "react-native";
import { Box, Text } from "@gluestack-ui/themed";
import JobCard from "../components/JobCard";
import AppLayout from "../layouts/AppLayout";
import { useAuth } from "../context/AuthContext";
import { queryApi } from "../api/api";

export default function HomeScreen() {
  const user = useAuth();
  const [jobs, setJobs] = useState<any[]>([]);
  const [nextUrl, setNextUrl] = useState<string | null>("/api/jobs/?page=1");
  const [loadingMore, setLoadingMore] = useState(false);
  const [initialLoading, setInitialLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const isMounted = useRef(false);

  // Fetch jobs page
  const fetchJobs = async (url: string) => {
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
      setJobs((prev) => [...prev, ...data.results]);
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
    if (!isMounted.current) {
      fetchJobs("/api/jobs/?page=1&user=" + user.id);
      isMounted.current = true;
    }
  }, []);

  const handleEndReached = () => {
    if (nextUrl && !loadingMore) {
      fetchJobs(nextUrl);
    }
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
      <Box
        flex={1}
        justifyContent="center"
        alignItems="center"
        bg="$backgroundDark950"
      >
        <Text color="$red500">Error fetching jobs</Text>
      </Box>
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
        renderItem={({ item }) => <JobCard job={item} />}
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
