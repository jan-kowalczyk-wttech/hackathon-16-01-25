import { useState, useCallback } from 'react';
import { StyleSheet, View, FlatList, RefreshControl, Text } from 'react-native';
import { useFocusEffect } from 'expo-router';
import SearchBar from '../(components)/common/SearchBar';
import OfferCard from '../(components)/marketplace/OfferCard';
import { fetchOffers } from '../(services)/api/offers';
import type { Offer } from '../(types)/offer.types';

export default function MarketplaceScreen() {
  const [offers, setOffers] = useState<Offer[]>([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [refreshing, setRefreshing] = useState(false);

  const loadOffers = async () => {
    const data = await fetchOffers();
    setOffers(data);
  };

  const onRefresh = async () => {
    setRefreshing(true);
    await loadOffers();
    setRefreshing(false);
  };

  useFocusEffect(
    useCallback(() => {
      loadOffers();
    }, [])
  );

  const filteredOffers = offers.filter(offer =>
    offer.title.toLowerCase().includes(searchQuery.toLowerCase())
  );

  return (
    <View style={styles.container}>
      <SearchBar value={searchQuery} onChangeText={setSearchQuery} />
      <FlatList
        data={filteredOffers}
        renderItem={({ item }) => <OfferCard offer={item} />}
        keyExtractor={item => item.id}
        refreshControl={
          <RefreshControl refreshing={refreshing} onRefresh={onRefresh} />
        }
        contentContainerStyle={styles.list}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  list: {
    padding: 8,
  },
});
