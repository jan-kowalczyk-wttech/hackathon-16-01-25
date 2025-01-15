import { useState, useEffect } from 'react';
import { StyleSheet, View, Text, Image, ScrollView, TouchableOpacity, Dimensions } from 'react-native';
import { useLocalSearchParams, router } from 'expo-router';
import { MaterialIcons } from '@expo/vector-icons';
import { mockOffers } from '../(services)/mock/mockOffers';

const { width } = Dimensions.get('window');

export default function OfferDetailsScreen() {
  const { id } = useLocalSearchParams<{ id: string }>();
  const [currentImageIndex, setCurrentImageIndex] = useState(0);

  // In a real app, you would fetch this from an API
  const offer = mockOffers.find(o => o.id === id);

  // Update the header title when the offer is loaded
  useEffect(() => {
    if (offer) {
      router.setParams({
        headerTitle: offer.title
      });
    }
  }, [offer]);

  if (!offer) {
    return (
      <View style={styles.container}>
        <Text>Offer not found</Text>
      </View>
    );
  }

  return (
    <ScrollView style={styles.container}>
      {/* Image Carousel */}
      <View style={styles.carousel}>
        <ScrollView
          horizontal
          pagingEnabled
          showsHorizontalScrollIndicator={false}
          onScroll={(e) => {
            const offset = e.nativeEvent.contentOffset.x;
            setCurrentImageIndex(Math.round(offset / width));
          }}
        >
          {offer.images.map((image, index) => (
            <Image
              key={index}
              source={{ uri: image }}
              style={styles.image}
              resizeMode="cover"
            />
          ))}
        </ScrollView>
        
        {/* Image Indicators */}
        <View style={styles.indicators}>
          {offer.images.map((_, index) => (
            <View
              key={index}
              style={[
                styles.indicator,
                index === currentImageIndex && styles.indicatorActive
              ]}
            />
          ))}
        </View>
      </View>

      {/* Offer Details */}
      <View style={styles.details}>
        <Text style={styles.title}>{offer.title}</Text>
        <Text style={styles.price}>${offer.price.toFixed(2)}</Text>
        
        <View style={styles.infoRow}>
          <MaterialIcons name="location-on" size={20} color="#666" />
          <Text style={styles.location}>{offer.location}</Text>
        </View>
        
        <View style={styles.infoRow}>
          <MaterialIcons name="info" size={20} color="#666" />
          <Text style={styles.condition}>Condition: {offer.condition}</Text>
        </View>

        <Text style={styles.sectionTitle}>Description</Text>
        <Text style={styles.description}>{offer.description}</Text>

        <Text style={styles.sectionTitle}>Seller</Text>
        <View style={styles.sellerInfo}>
          <MaterialIcons name="account-circle" size={40} color="#666" />
          <Text style={styles.sellerName}>{offer.seller.name}</Text>
        </View>

        {/* Buy Button */}
        <TouchableOpacity 
          style={styles.buyButton}
          onPress={() => {
            // Handle purchase logic
            alert('Purchase functionality coming soon!');
          }}
        >
          <Text style={styles.buyButtonText}>Buy Now</Text>
        </TouchableOpacity>
      </View>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
  },
  carousel: {
    height: width,
    position: 'relative',
  },
  image: {
    width: width,
    height: width,
  },
  indicators: {
    flexDirection: 'row',
    position: 'absolute',
    bottom: 16,
    alignSelf: 'center',
  },
  indicator: {
    width: 8,
    height: 8,
    borderRadius: 4,
    backgroundColor: 'rgba(255, 255, 255, 0.4)',
    marginHorizontal: 4,
  },
  indicatorActive: {
    backgroundColor: '#fff',
  },
  details: {
    padding: 16,
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    marginBottom: 8,
  },
  price: {
    fontSize: 28,
    fontWeight: 'bold',
    color: '#007AFF',
    marginBottom: 16,
  },
  infoRow: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 8,
  },
  location: {
    fontSize: 16,
    color: '#666',
    marginLeft: 8,
  },
  condition: {
    fontSize: 16,
    color: '#666',
    marginLeft: 8,
    textTransform: 'capitalize',
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: '600',
    marginTop: 16,
    marginBottom: 8,
  },
  description: {
    fontSize: 16,
    lineHeight: 24,
    color: '#333',
  },
  sellerInfo: {
    flexDirection: 'row',
    alignItems: 'center',
    marginTop: 8,
  },
  sellerName: {
    fontSize: 16,
    marginLeft: 12,
  },
  buyButton: {
    backgroundColor: '#007AFF',
    padding: 16,
    borderRadius: 8,
    alignItems: 'center',
    marginTop: 24,
  },
  buyButtonText: {
    color: '#fff',
    fontSize: 18,
    fontWeight: '600',
  },
}); 