import 'dotenv/config';

export default {
  expo: {
    // ...existing config...
    name: "NextJob AI", //
    slug: "nextjob-ai",
    plugins: ["expo-web-browser"],
    userInterfaceStyle: "automatic",
    ios: {
      bundleIdentifier: "ai.nextjob.client",
    },
    extra: {
      BASE_URL: process.env.BASE_URL,
      GOOGLE_CLIENT_ID: process.env.GOOGLE_CLIENT_ID,
      IOS_GOOGLE_CLIENT_ID: process.env.IOS_GOOGLE_CLIENT_ID,
    },
  },
};