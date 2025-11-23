package com.example.carrot_backend.item.infrastructure.mapper;

import com.example.carrot_backend.item.domain.ItemEntity;
import com.example.carrot_backend.item.domain.ItemReader;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;

@Repository
@RequiredArgsConstructor
public class ItemReaderImpl implements ItemReader {

    private final ItemRepository itemRepository;

    @Override
    public Optional<ItemEntity> getItemById(Long itemId) {
        return itemRepository.findById(itemId);
    }

    @Override
    public List<ItemEntity> findAllBySellerIdOrderByCreatedAtDesc(Long sellerId) {
        return itemRepository.findAllBySellerIdOrderByCreatedAtDesc(sellerId);
    }
}
