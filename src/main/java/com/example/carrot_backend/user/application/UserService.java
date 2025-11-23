package com.example.carrot_backend.user.application;

import com.example.carrot_backend.item.controller.dto.ItemListResponse;
import com.example.carrot_backend.item.domain.ItemReader;
import com.example.carrot_backend.user.controller.UserController;
import com.example.carrot_backend.user.controller.dto.MyPageResponseDto;
import com.example.carrot_backend.user.domain.UserReader;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

import java.util.stream.Collectors;

@Service
@RequiredArgsConstructor
public class UserService {

    private final UserReader userReader;

    private final ItemReader itemReader;

    public MyPageResponseDto getMyPage(String email){

        var user = userReader.findByEmail(email).orElseThrow(() -> new RuntimeException("User not found"));

        var items = itemReader.findAllBySellerIdOrderByCreatedAtDesc(user.getId());

        var itemsDto = items.stream()
                .map(ItemListResponse::from)
                .toList();

        return new MyPageResponseDto(user, itemsDto);



    }

}
