import { Stack, Tabs } from "expo-router";
import { MaterialIcons } from "@expo/vector-icons";

export default function AppLayout() {
  return (
    <Stack>
      <Stack.Screen
        name="(tabs)"
        options={{ headerShown: false }}
      />
      <Stack.Screen
        name="offer/[id]"
        options={{
          headerTitle: "Item Details",
        }}
      />
    </Stack>
  );
}
