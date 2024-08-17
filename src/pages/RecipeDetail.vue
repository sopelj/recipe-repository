<script setup lang="ts">
import type { User } from "@/types/users";
import type { Recipe, Ingredient } from "@/types/recipes";

import { ref } from "vue";
import { router } from "@inertiajs/vue3";
import { useI18n } from "vue-i18n";
import { useShare } from "@/composables/share";

import { breakpointsTailwind, useBreakpoints } from '@vueuse/core';


import NutritionalInformation from "@/components/NutritionalInformation.vue";
import HeadSection from "@/layouts/HeadSection.vue";
import UserAvatar from "@/components/UserAvatar.vue";
import RecipeDurations from "@/components/RecipeDurations.vue";
import RecipeSource from "@/components/RecipeSource.vue";
import KeepAwake from "@/components/KeepAwake.vue";
import DescriptionItem from "@/components/DescriptionItem.vue";

interface FormErrors {
  servings?: string[];
}

const props = defineProps<{
  recipe: Recipe;
  ingredients: Ingredient[];
  servings: number;
  errors: FormErrors | null;
  user?: User;
  userRating: number | null;
}>();

const { t } = useI18n();

const breakpoints = useBreakpoints(breakpointsTailwind);
const isAboveSmall = breakpoints.greater("sm");

const { share, canShare } = useShare();
const shareRecipe = async () => {
  await share(props.recipe.name, t("recipe.share", { name: props.recipe.name }));
};

const servingAmount = ref<number>(props.servings || 1);
const formError = ref<string | undefined>();

const updateServings = (multiplier: number) => {
  if (!servingAmount.value) {
    servingAmount.value = props.servings;
    return;
  }
  const newValue = servingAmount.value * multiplier;
  if (newValue > 100 || newValue < 0.125) {
    formError.value = "Serving value must be between 0.125 and 100";
    servingAmount.value = props.servings;
    return;
  }
  // TODO: use `useForm` when django-inertia supports it.
  router.visit(`${window.location.pathname}?servings=${newValue}`, {
    only: ["ingredients", "servings"],
  });
};
</script>

<template>
  <HeadSection :title="recipe.name" />
  <div
    class="container mx-auto px-4"
    itemscope
    itemtype="https://schema.org/Recipe"
  >
    <div class="grid grid-cols-12 gap-4">
      <div class="col-span-12 sm:col-span-9 md:col-span-8">
        <div class="flex flex-wrap sm:flex-nowrap items-center mb-4 ">
          <h1
            class="text-4xl cursive flex-grow"
            itemprop="name"
          >
            {{ recipe.name }}
          </h1>
          <Rating
            v-tooltip="t('recipe.ratings', recipe.num_ratings)"
            :model-value="userRating || recipe.avg_rating"
            :readonly="true"
            class="flex-grow sm:flex-grow-0"
          />
          <Button
            v-if="canShare"
            v-tooltip="t('recipe.share')"
            icon="pi pi-share-alt"
            class="ml-1"
            text
            @click="shareRecipe"
          />
        </div>
        <div
          v-if="recipe.image_url"
          class="overflow-clip p-card mt-4 sm:hidden"
        >
          <img
            :src="recipe.image_url"
            :alt="recipe.name"
          />
        </div>
        <DescriptionItem
          v-if="recipe.categories"
          :label="t('recipe.categories')"
        >
          <Tag
            v-for="c in recipe.categories"
            :key="c.slug"
            class="mx-1"
            severity="secondary"
          >
            {{ c.name }}
          </Tag>
        </DescriptionItem>
        <DescriptionItem :label="t('recipe.yields')">
          <span
            v-if="recipe.yield_unit"
            itemprop="recipeYield"
            >{{ recipe.yield_amount }} {{ recipe.yield_unit }} ({{ t("recipe.servings", servings) }})</span
          >
          <span v-else>{{ t("recipe.servings", servings) }}</span>
        </DescriptionItem>
        <DescriptionItem :label="t('recipe.added_by')">
          <UserAvatar
            :user="recipe.added_by"
            size="normal"
          />
          <span class="pl-2">{{
            recipe.added_by.id === user?.id ? t("users.me") : recipe.added_by.full_name
          }}</span>
        </DescriptionItem>
        <DescriptionItem
          v-if="recipe.source"
          :label="t('recipe.from')"
        >
          <RecipeSource
            :source="recipe.source"
            :value="recipe.source_value"
          />
        </DescriptionItem>
        <div
          v-if="recipe.description"
          class="mt-2 pb-5"
          itemprop="description"
        >
          <Divider />
          {{ recipe.description }}
        </div>
        <RecipeDurations :prep-time="recipe.prep_time" :cook-time="recipe.cook_time" :total-time="recipe.total_time" />
        <NutritionalInformation
          v-if="recipe.nutrition && !isAboveSmall"
          :nutrition="recipe.nutrition"
          :servings="servings"
          class="mt-4"
        />
        <div class="ingredients">
          <card>
            <template #title>
              <div class="flex flex-row items-center">
                <h2 class="text-xxl grow w-100 mr-2">{{ t("recipe.ingredients") }}</h2>
                <div class="grow-0 ml-4">
                  <InputGroup class="grow-0">
                    <Button
                      :disabled="!servingAmount || servingAmount / 2 <= 0.125"
                      @click="updateServings(0.5)"
                      >{{ t("recipe.scale_halve") }}</Button
                    >
                    <InputNumber
                      v-model="servingAmount"
                      placeholder="servings"
                      :min="0.125"
                      :max="100"
                      input-class="text-center pa-0"
                      :fluid="true"
                      @update="updateServings(1)"
                    />
                    <Button
                      :disabled="servingAmount * 2 >= 100"
                      @click="updateServings(2)"
                      >{{ t("recipe.scale_double") }}</Button
                    >
                  </InputGroup>
                  <Message v-if="errors?.servings?.length" severity="error">{{ errors.servings[0] }}</Message>
                </div>
              </div>
            </template>
            <template #content>
              <ul>
                <li
                  v-for="ingredient in ingredients"
                  :key="ingredient.id"
                >
                  <i18n-t
                    keypath="recipe.ingredient"
                    tag="span"
                  >
                    <template #amount>{{ ingredient.amount_display }}</template>
                    <template #ingredient>
                      <strong>{{ ingredient.food_display }}</strong>
                    </template>
                  </i18n-t>
                  <span
                    v-if="ingredient.qualifier"
                    class="qualifier"
                    >{{ t("recipe.ingredient_qualifier", { qualifier: ingredient.qualifier}) }}</span
                  >
                  <span
                    v-if="ingredient.optional"
                    class="optional"
                    >{{ t("recipe.ingredient_optional") }}</span
                  >
                  <span v-if="ingredient.note">{{ t("recipe.ingredient_note", { note: ingredient.note }) }}</span>
                </li>
              </ul>
            </template>
          </card>
        </div>
      </div>
      <div class="col-span-12 sm:col-span-3 md:col-span-4">
        <div
          v-if="recipe.image_url"
          class="overflow-clip p-card hidden sm:flex"
        >
          <img
            :src="recipe.image_url"
            :alt="recipe.name"
            class="w-full"
          />
        </div>
        <NutritionalInformation
          v-if="recipe.nutrition && isAboveSmall"
          :nutrition="recipe.nutrition"
          :servings="servings"
          class="mt-4"
        />
      </div>
      <div class="col-span-12 md:col-span-8">
        <div class="flex flex-row mb-2">
          <h2 class="text-xl flex-grow">{{ t("recipe.directions") }}</h2>
          <KeepAwake />
        </div>
        <Panel
          v-for="(step, i) in recipe.steps"
          :key="i"
          toggleable
          class="mb-2"
          :header="t('recipe.step_title', { step: i + 1 })"
          itemprop="recipeInstructions"
        >
          {{ step }}
        </Panel>
      </div>
    </div>
  </div>
</template>
