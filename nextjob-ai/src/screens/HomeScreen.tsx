import React from "react";
import { FlatList } from "react-native";
import { Box, Text, Pressable } from "@gluestack-ui/themed";
import Swipeable from "react-native-gesture-handler/Swipeable";
import { TrashIcon } from "lucide-react-native";
import AppLayout from "../layouts/AppLayout";
import JobCard from "../components/JobCard";
import Loader from "../components/Loader";
import { useAuth } from "../context/AuthContext";
import { useNavigation } from "@react-navigation/native";
import { useApi, useApiMutation } from "../api/api";
import { JobOffer } from "../types/JobType";

type JobOfferPage = {
  count: number;
  next: string | null;
  previous: string | null;
  results: JobOffer[];
};

const PAGE_SIZE = 20;

export default function HomeScreen() {
  const user = useAuth();
  const navigation = useNavigation<any>();

  React.useEffect(() => {
    if (!user) {
      navigation.reset({ index: 0, routes: [{ name: "Login" }] });
      return;
    }
    if (!user.username || user.username.trim() === "") {
      navigation.reset({
        index: 0,
        routes: [{ name: "CompleteProfile", params: { user } }],
      });
    }
  }, [user]);

  const [jobs, setJobs] = React.useState<JobOffer[]>([]);
  const [nextUrl, setNextUrl] = React.useState<string | null>(null);
  const [error, setError] = React.useState<string | null>(null);

  const initialUrl = React.useMemo(() => {
    const base = `/job-offers?limit=${PAGE_SIZE}&offset=0`;
    return user?.id ? `${base}&user=${user.id}` : base;
  }, [user?.id]);

  const toRelative = (url: string | null) =>
    url ? url.replace(/^http(s)?:\/\/[^/]+/, "") : null;

  const initialQuery = useApi<JobOfferPage>(
    { url: initialUrl, options: { method: "GET" } },
    {
      enabled: Boolean(user?.id),
      onError: (err: any) => setError(err?.message || "Unknown error"),
    },
    [
      "job-offers",
      ["user", user?.id ?? null],
      ["limit", PAGE_SIZE],
      ["offset", 0],
    ]
  );

  // When first page arrives, populate jobs and next
  React.useEffect(() => {
    if (initialQuery.data) {
      setJobs(initialQuery.data.results ?? []);
      setNextUrl(toRelative(initialQuery.data.next));
      setError(null);
    }
  }, [initialQuery.data]);

  const loadMoreMutation = useApiMutation<string, JobOfferPage>(
    (url) => ({ url, options: { method: "GET" } }),
    {
      onSuccess: (data) => {
        setJobs((prev) => [...prev, ...(data.results ?? [])]);
        setNextUrl(toRelative(data.next));
      },
      onError: (err: any) => setError(err?.message || "Unknown error"),
    }
  );

  const loadMore = React.useCallback(() => {
    if (nextUrl && !loadMoreMutation.isPending) {
      loadMoreMutation.mutate(nextUrl);
    }
  }, [nextUrl, loadMoreMutation.isPending]);

  const deleteMutation = useApiMutation<number, void>(
    (jobId) => ({ url: `/job-offers/${jobId}`, options: { method: "DELETE" } }),
    undefined,
    ["job-offers"]
  );

  const handleDeleteUI = (jobId: number) => {
    setJobs((prev) => prev.filter((j) => j.id !== jobId)); // optimistic
    deleteMutation.mutate(jobId, {
      onError: () => initialQuery.refetch(), // rollback by refetching first page
    });
  };

  const isInitialLoading = initialQuery.isLoading && !initialQuery.data;
  const isFetchingMore = loadMoreMutation.isPending;
  const isFetchingInitial = initialQuery.isFetching; // bg refetch

  if (!user) return null;

  if (isInitialLoading) {
    return <Loader />;
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
              Welcome, {user.username || "there"}!
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
          <Pressable onPress={() => initialQuery.refetch()}>
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
            Welcome, {user.username || "there"}!
          </Text>
          <Text color="$coolGray200" fontSize="$md" mt={2} textAlign="center">
            Discover your next opportunity. Browse the latest job offers below.
          </Text>
        </Box>
      </Box>

      <FlatList
        data={jobs}
        keyExtractor={(item) => String(item.id)}
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
        onEndReachedThreshold={0.5}
        onEndReached={() => nextUrl && loadMore()}
        ListFooterComponent={
          isFetchingMore || isFetchingInitial ? (
            <Box py={4} alignItems="center">
              <Text>Loading…</Text>
            </Box>
          ) : null
        }
      />
    </AppLayout>
  );
}
