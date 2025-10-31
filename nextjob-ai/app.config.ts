import 'dotenv/config';

export default {
  expo: {
    name: "NextJob AI",
    slug: "nextjob-ai",
    version: "1.0.0",
    orientation: "portrait",
    icon: "./assets/icon.png",
    userInterfaceStyle: "automatic",
    // newArchEnabled: false,
    splash: {
      image: "./assets/splash-icon.png",
      resizeMode: "contain",
      backgroundColor: "#ffffff"
    },
    ios: {
      supportsTablet: true,
      bundleIdentifier: "ai.nextjob.client",
    },
    android: {
      adaptiveIcon: {
        foregroundImage: "./assets/adaptive-icon.png",
        backgroundColor: "#ffffff"
      },
      edgeToEdgeEnabled: true
    },
    web: {
      favicon: "./assets/favicon.png"
    },
    plugins: ["expo-web-browser"],
    extra: {
      BASE_URL: process.env.BASE_URL,
      GOOGLE_CLIENT_ID: process.env.GOOGLE_CLIENT_ID,
      IOS_GOOGLE_CLIENT_ID: process.env.IOS_GOOGLE_CLIENT_ID,
    },
  },
};