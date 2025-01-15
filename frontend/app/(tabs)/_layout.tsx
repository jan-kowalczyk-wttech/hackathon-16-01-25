import { Tabs } from "expo-router";
import { MaterialIcons } from "@expo/vector-icons";
import { Platform, Text } from "react-native";
import { colors } from "../theme/colors";

// Custom header title component
function HeaderTitle({ title }: { title: string }) {
  return (
    <Text 
      style={{
        fontSize: 24,
        fontWeight: '700',
        color: colors.text.primary,
        letterSpacing: -0.5,
        paddingVertical: 8,
        ...Platform.select({
          ios: { fontFamily: '-apple-system' },
          android: { fontFamily: 'sans-serif-medium' },
        }),
      }}
    >
      {title}
    </Text>
  );
}

export default function TabsLayout() {
  return (
    <Tabs
      screenOptions={{
        tabBarActiveTintColor: colors.primary,
        tabBarInactiveTintColor: colors.gray[400],
        headerShown: true,
        headerStyle: {
          backgroundColor: colors.surface,
          elevation: 0,
          shadowOpacity: 0,
          borderBottomWidth: 1,
          borderBottomColor: colors.border,
        },
        headerTitleAlign: 'left',
        headerShadowVisible: false,
        headerTitleContainerStyle: {
          paddingHorizontal: 16,
        },
        tabBarStyle: {
          backgroundColor: colors.surface,
          borderTopWidth: 1,
          borderTopColor: colors.border,
          elevation: 0,
          shadowOpacity: 0,
          height: Platform.OS === 'ios' ? 88 : 64,
          paddingBottom: Platform.OS === 'ios' ? 28 : 12,
          paddingTop: 12,
        },
        tabBarLabelStyle: {
          fontSize: 12,
          fontWeight: '500',
        },
        tabBarHideOnKeyboard: true,
      }}
    >
      <Tabs.Screen
        name="index"
        options={{
          title: "Discover",
          headerTitle: () => <HeaderTitle title="Discover" />,
          tabBarIcon: ({ color, size }) => (
            <MaterialIcons name="explore" size={size} color={color} />
          ),
        }}
      />
      <Tabs.Screen
        name="chat/index"
        options={{
          title: "Sell",
          headerTitle: () => <HeaderTitle title="New Listing" />,
          tabBarIcon: ({ color, size }) => (
            <MaterialIcons name="add-circle" size={size} color={color} />
          ),
        }}
      />
      <Tabs.Screen
        name="settings/index"
        options={{
          title: "Profile",
          headerTitle: () => <HeaderTitle title="Profile" />,
          tabBarIcon: ({ color, size }) => (
            <MaterialIcons name="person" size={size} color={color} />
          ),
        }}
      />
    </Tabs>
  );
} 