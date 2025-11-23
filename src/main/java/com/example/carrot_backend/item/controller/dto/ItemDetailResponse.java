package com.example.carrot_backend.item.controller.dto;

import com.example.carrot_backend.item.domain.ItemEntity;
import lombok.Getter;
import org.hibernate.cache.spi.support.AbstractReadWriteAccess;
import org.springframework.format.annotation.DateTimeFormat;

import java.time.format.DateTimeFormatter;

@Getter
public class ItemDetailResponse {

    private Long id;
    private String title;
    private String category;
    private String createdAt;
    private Integer price;
    private String content;
    private String region;
    private String thumbnail;

    private String sellerNickname;
    private String sellerProfileUrl;
    private Double sellerMannerTemp;

    public ItemDetailResponse(ItemEntity item) {
        this.id = item.getId();
        this.title = item.getTitle();
        this.category = item.getCategory();
        this.createdAt = item.getCreatedAt().format(DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm"));
        this.price = item.getPrice();
        this.content = item.getContent();
        this.region = item.getRegion();
        this.thumbnail = item.getThumbnailUrl();
        this.sellerNickname = item.getSeller().getNickname();
        this.sellerMannerTemp = item.getSeller().getMannerTemp();
        this.sellerProfileUrl = item.getSeller().getProfileUrl();

    }

}
