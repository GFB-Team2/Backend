package com.example.carrot_backend.item.infrastructure.mapper;

import com.example.carrot_backend.item.domain.ItemEntity;
import org.hibernate.cache.spi.support.AbstractReadWriteAccess;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;

@Repository
public interface ItemRepository extends JpaRepository<ItemEntity,Long> {

    Optional<ItemEntity> findById(Long itemId);


    List<ItemEntity> findAllBySellerIdOrderByCreatedAtDesc(Long sellerId);

}
