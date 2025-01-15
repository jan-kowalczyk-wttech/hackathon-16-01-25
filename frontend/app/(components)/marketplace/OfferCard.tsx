import { StyleSheet, View, Text, Image, Pressable } from 'react-native';
import { router } from 'expo-router';
import { Offer } from '../../(types)/offer.types';

interface OfferCardProps {
  offer: Offer;
}

export function OfferCard({ offer }: OfferCardProps) {
  const handlePress = () => {
    // Navigate to the offer details screen
    router.push({
      pathname: "/offer/[id]",
      params: { id: offer.id }
    });
  };

  return (
    <Pressable
      style={styles.container}
      onPress={handlePress}
    >
      <Image source={{ uri: offer.images[0] }} style={styles.image} />
      <View style={styles.info}>
        <Text style={styles.title} numberOfLines={1}>
          {offer.title}
        </Text>
        <Text style={styles.price}>${offer.price.toFixed(2)}</Text>
        <Text style={styles.location} numberOfLines={1}>
          {offer.location}
        </Text>
      </View>
    </Pressable>
  );
}

const styles = StyleSheet.create({
  container: {
    backgroundColor: 'white',
    borderRadius: 12,
    margin: 8,
    overflow: 'hidden',
    elevation: 2,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
  },
  image: {
    width: '100%',
    height: 200,
    resizeMode: 'cover',
  },
  info: {
    padding: 12,
  },
  title: {
    fontSize: 16,
    fontWeight: '600',
    marginBottom: 4,
  },
  price: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#007AFF',
    marginBottom: 4,
  },
  location: {
    fontSize: 14,
    color: '#666',
  },
});

export default OfferCard; 