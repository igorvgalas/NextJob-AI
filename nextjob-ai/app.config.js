import 'dotenv/config';

export default {
  expo: {
    // ...existing config...
    extra: {
      BASE_URL: process.env.BASE_URL,
    },
  },
};