package com.example.carrot_backend.item.domain;

import java.util.List;
import java.util.Optional;

public interface ItemReader {

    Optional<ItemEntity> getItemById(Long itemId);

    List<ItemEntity> findAllBySellerIdOrderByCreatedAtDesc(Long sellerId);

}
