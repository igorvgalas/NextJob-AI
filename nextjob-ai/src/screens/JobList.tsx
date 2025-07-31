// import React from 'react';
// import { View, Text, FlatList, Linking } from 'react-native';
// import { useQuery } from '@tanstack/react-query';
// import axios from 'axios';

// const fetchJobs = async () => {
//   const { data } = await axios.get('http://192.168.100.23:8000/api/jobs/');
//   return data;
// };

// export default function JobList() {
//   const { data, isLoading, error } = useQuery({
//     queryKey: ['jobs'],
//     queryFn: fetchJobs,
//   });

//   if (isLoading) return <Text>Loading jobs...</Text>;
//   if (error) return <Text>Error fetching jobs</Text>;

//   return (
//     <FlatList
//       data={data}
//       style={{ padding: 10 }}
//       showsVerticalScrollIndicator={false}
//       keyExtractor={(item) => item.id}
//       renderItem={({ item }) => (
//         <View style={{ marginVertical: 10 }}>
//           <Text style={{ fontWeight: 'bold' }}>{item.title}</Text>
//           <Text>{item.company}</Text>
//           <Text>{item.location}</Text>
//           <Text>{item.description}</Text>
//           <Text style={{ color: 'blue' }} onPress={() => Linking.openURL(item.apply_link)}>
//             {item.apply_link}
//           </Text>
//         </View>
//       )}
//     />
//   );
// }

// import React from "react";
// import { View, Text, FlatList, Linking, StyleSheet } from "react-native";
// import { useQuery } from "@tanstack/react-query";
// import axios from "axios";

// const fetchJobs = async () => {
//   const { data } = await axios.get("http://192.168.100.23:8000/api/jobs/");
//   return data;
// };

// export default function JobList() {
//   const { data, isLoading, error } = useQuery({
//     queryKey: ["jobs"],
//     queryFn: fetchJobs,
//   });

//   if (isLoading) return <Text style={styles.message}>Loading jobs...</Text>;
//   if (error) return <Text style={styles.message}>Error fetching jobs</Text>;

//   return (
//     <FlatList
//       data={data}
//       contentContainerStyle={styles.listContainer}
//       showsVerticalScrollIndicator={false}
//       keyExtractor={(item) => item.id.toString()}
//       renderItem={({ item }) => (
//         <View style={styles.card}>
//           <Text style={styles.title}>{item.title}</Text>
//           <Text style={styles.company}>{item.company}</Text>
//           <Text style={styles.location}>{item.location}</Text>
//           <Text style={styles.description}>{item.description}</Text>
//           <Text
//             style={styles.link}
//             onPress={() => Linking.openURL(item.apply_link)}
//           >
//             Apply Link
//           </Text>
//         </View>
//       )}
//     />
//   );
// }

// const styles = StyleSheet.create({
//   message: {
//     padding: 20,
//     textAlign: "center",
//     fontSize: 16,
//   },
//   listContainer: {
//     padding: 16,
//     backgroundColor: "#f0f2f5",
//   },
//   card: {
//     backgroundColor: "white",
//     borderRadius: 12,
//     padding: 16,
//     marginBottom: 12,
//     shadowColor: "#000",
//     shadowOpacity: 0.1,
//     shadowRadius: 6,
//     shadowOffset: { width: 0, height: 3 },
//     elevation: 4,
//   },
//   title: {
//     fontSize: 18,
//     fontWeight: "bold",
//     color: "#333",
//   },
//   company: {
//     fontSize: 16,
//     marginTop: 4,
//     color: "#555",
//   },
//   location: {
//     fontSize: 14,
//     color: "#888",
//     marginBottom: 6,
//   },
//   description: {
//     fontSize: 14,
//     color: "#444",
//     marginBottom: 10,
//   },
//   link: {
//     color: "#1e90ff",
//     textDecorationLine: "underline",
//   },
// });

import React from 'react';
import { View, Text, FlatList, Linking, StyleSheet } from 'react-native';
import { useQuery } from '@tanstack/react-query';
import axios from 'axios';

const fetchJobs = async () => {
  const { data } = await axios.get('http://192.168.100.23:8000/api/jobs/');
  return data;
};

export default function JobList() {
  const { data, isLoading, error } = useQuery({
    queryKey: ['jobs'],
    queryFn: fetchJobs,
  });

  if (isLoading) return <Text style={styles.message}>Loading jobs...</Text>;
  if (error) return <Text style={styles.message}>Error fetching jobs</Text>;

  return (
    <FlatList
      data={data}
      contentContainerStyle={styles.listContainer}
      showsVerticalScrollIndicator={false}
      keyExtractor={(item) => item.id.toString()}
      renderItem={({ item }) => (
        <View style={styles.card}>
          <Text style={styles.title}>{item.title}</Text>
          <Text style={styles.company}>{item.company}</Text>
          <Text style={styles.location}>{item.location}</Text>
          <Text style={styles.description}>{item.description}</Text>
          <Text
            style={styles.link}
            onPress={() => Linking.openURL(item.apply_link)}>
            Open Job Link
          </Text>
        </View>
      )}
    />
  );
}

const styles = StyleSheet.create({
  message: {
    padding: 20,
    textAlign: 'center',
    fontSize: 16,
    color: '#fff',
    backgroundColor: '#121212',
  },
  listContainer: {
    padding: 16,
    backgroundColor: '#121212', // Dark background
  },
  card: {
    backgroundColor: '#1e1e1e', // Dark gray card
    borderRadius: 12,
    padding: 16,
    marginBottom: 12,
  },
  title: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#ffffff',
    marginBottom: 4,
  },
  company: {
    fontSize: 16,
    color: '#cccccc',
  },
  location: {
    fontSize: 14,
    color: '#999999',
    marginBottom: 8,
  },
  description: {
    fontSize: 14,
    color: '#dddddd',
    marginBottom: 10,
  },
  link: {
    color: '#1e90ff',
    textDecorationLine: 'underline',
  },
});