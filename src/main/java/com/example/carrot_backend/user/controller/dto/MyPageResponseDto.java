package com.example.carrot_backend.user.controller.dto;

import com.example.carrot_backend.item.controller.dto.ItemListResponse;
import com.example.carrot_backend.user.domain.UserEntity;
import lombok.*;

import java.util.List;

@Getter
@Setter
@ToString
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class MyPageResponseDto {

    private Long userId;

    private String nickname;

    private Double mannerTemp;

    private List<ItemListResponse> myItems;

    private String profileUrl;

    public MyPageResponseDto(UserEntity user, List<ItemListResponse> myItems) {
        this.userId = user.getId();
        this.nickname = user.getNickname();
        this.mannerTemp = user.getMannerTemp();
        this.myItems = myItems;
        this.profileUrl = user.getProfileUrl();
    }



}
