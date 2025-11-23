package com.example.carrot_backend.item.domain;

import com.example.carrot_backend.user.domain.UserEntity;
import jakarta.persistence.*;
import lombok.AccessLevel;
import lombok.Builder;
import lombok.Getter;
import lombok.NoArgsConstructor;
import org.hibernate.annotations.CreationTimestamp;

import java.time.LocalDateTime;

@Entity
@Getter
@NoArgsConstructor(access = AccessLevel.PROTECTED)
@Table(name = "items")
public class ItemEntity {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "item_id")
    private Long id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "seller_id", nullable = false)
    private UserEntity seller;

    @Column(nullable = false, length = 100)
    private String title;

    @Column(nullable = false)
    private Integer price;

    @Column(nullable = false, columnDefinition = "TEXT")
    private String content;

    @Column(nullable = false)
    private String region;

    @Column(nullable = false)
    private String category;

    private String thumbnailUrl;

    @CreationTimestamp
    private LocalDateTime createdAt;

    @Builder
    public ItemEntity(UserEntity seller, String title, Integer price, String content, String region, String category, String thumbnailUrl) {
        this.seller = seller;
        this.title = title;
        this.price = price;
        this.content = content;
        this.region = region;
        this.category = category;
        this.thumbnailUrl = thumbnailUrl;
    }


}
