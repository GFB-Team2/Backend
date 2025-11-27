package com.example.carrot_backend.item.infrastructure;

import com.example.carrot_backend.item.domain.ItemEntity;
import com.example.carrot_backend.item.domain.ItemWriter;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Repository;

@Repository
@RequiredArgsConstructor
public class ItemWriterImpl implements ItemWriter {


    private final ItemRepository itemRepository;

    @Override
    public void save(ItemEntity item) {
        itemRepository.save(item);
    }
}
