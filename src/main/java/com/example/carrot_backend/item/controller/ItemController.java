package com.example.carrot_backend.item.controller;

import com.example.carrot_backend.common.dto.ApiResponse;
import com.example.carrot_backend.item.application.ItemService;
import com.example.carrot_backend.item.controller.dto.ItemCreateRequestDto;
import com.example.carrot_backend.item.controller.dto.ItemDetailResponse;
import com.example.carrot_backend.item.controller.dto.ItemListResponse;
import com.example.carrot_backend.item.controller.dto.ItemSearchCondDto;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpSession;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@Slf4j
@RestController
@RequestMapping("/api/items")
@RequiredArgsConstructor
public class ItemController {

    private final ItemService itemService;

    @GetMapping
    public ResponseEntity<ApiResponse<List<ItemListResponse>>> getItems(
            @ModelAttribute ItemSearchCondDto itemSearchCondDto
    ) {
        log.info("ItemSearchDto: {}, {}, {}", itemSearchCondDto.getKeyword(), itemSearchCondDto.getRegions(), itemSearchCondDto.getCategories());
        var response = itemService.getItems(itemSearchCondDto);
        return ResponseEntity.ok(ApiResponse.success("상품 목록 조회 성공",response));
    }

    @GetMapping("/{itemId}")
    public ResponseEntity<ApiResponse<ItemDetailResponse>> getItemDetail(
            @PathVariable Long itemId
    ){
        var response = itemService.getItemDetail(itemId);
        return ResponseEntity.ok(ApiResponse.success("해당 상품 상세 조회", response));
    }

    @PostMapping
    public ResponseEntity<ApiResponse<Void>> createItem(
            @RequestBody @Valid ItemCreateRequestDto itemCreateRequestDto,
            HttpServletRequest request){


        HttpSession session = request.getSession(false);
        if (session == null || session.getAttribute("USER_EMAIL") == null) {
            throw new RuntimeException("상품 등록을 위해 로그인이 필요합니다.");
        }

        String email = (String) session.getAttribute("USER_EMAIL");

        itemService.createItem(email, itemCreateRequestDto);

        return ResponseEntity.ok(ApiResponse.success("상품 등록 완료", null));
    }

}
