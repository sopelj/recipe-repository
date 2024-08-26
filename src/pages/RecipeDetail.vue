<script setup lang="ts">
import type { Ingredient, Recipe } from "@/types/recipes";
import type { User } from "@/types/users";

import { Link } from "@inertiajs/vue3";
import { breakpointsTailwind, useBreakpoints } from "@vueuse/core";
import { useI18n } from "vue-i18n";

import { useShare } from "@/composables/share";

import BreadcrumbBar from "@/components/BreadcrumbBar.vue";
import DescriptionItem from "@/components/DescriptionItem.vue";
import FavouriteForm from "@/components/FavouriteForm.vue";
import IngredientList from "@/components/IngredientList.vue";
import KeepAwake from "@/components/KeepAwake.vue";
import NutritionalInformation from "@/components/NutritionalInformation.vue";
import RatingForm from "@/components/RatingForm.vue";
import RecipeDurations from "@/components/RecipeDurations.vue";
import RecipeSource from "@/components/RecipeSource.vue";
import RecipeYield from "@/components/RecipeYield.vue";
import ServingsForm from "@/components/ServingsForm.vue";
import UserAvatar from "@/components/UserAvatar.vue";
import HeadSection from "@/layouts/HeadSection.vue";

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
  userFavourite: boolean;
}>();

const { t } = useI18n();

const breakpoints = useBreakpoints(breakpointsTailwind);
const isAboveSmall = breakpoints.greater("sm");

const { share, canShare } = useShare();
const shareRecipe = async () => {
  await share(props.recipe.name, t("recipe.share_title", { name: props.recipe.name }));
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
        <div class="flex flex-wrap sm:flex-nowrap items-center mb-4">
          <h1
            class="text-4xl cursive flex-grow w-full sm:w-auto"
            itemprop="name"
          >
            {{ recipe.name }}
          </h1>
          <div class="flex-grow sm:flex-grow-0">
            <RatingForm
              :average-rating="recipe.avg_rating"
              :num-ratings="recipe.num_ratings"
              :user-rating="userRating"
              :disabled="!user"
              class="w-fit"
            />
          </div>
          <FavouriteForm
            v-if="user"
            :user-favourite="userFavourite"
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
        <BreadcrumbBar :current="recipe.name" />
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
          <RecipeYield
            v-if="recipe.yield_unit && recipe.yield_amount"
            :amount="recipe.yield_amount"
            :unit="recipe.yield_unit"
            :servings="servings"
            :base-servings="recipe.servings || 1"
          />
          <span v-else>{{ t("recipe.servings", servings) }}</span>
        </DescriptionItem>
        <DescriptionItem :label="t('recipe.added_by')">
          <UserAvatar
            :user="recipe.added_by"
            size="normal"
          />
          <span class="pl-2">
            {{ recipe.added_by.id === user?.id ? t("users.me") : recipe.added_by.full_name }}
          </span>
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
        <RecipeDurations
          :prep-time="recipe.prep_time"
          :cook-time="recipe.cook_time"
          :total-time="recipe.total_time"
        />
        <NutritionalInformation
          v-if="recipe.nutrition && !isAboveSmall"
          :nutrition="recipe.nutrition"
          :servings="servings"
          class="mt-4"
        />
        <div class="mt-4">
          <Card>
            <template #title>
              <div class="flex flex-row items-center">
                <h2 class="text-xxl grow w-100 mr-2">{{ t("recipe.ingredients") }}</h2>
                <ServingsForm :servings="servings || 1" />
              </div>
            </template>
            <template #content>
              <div v-if="recipe.parent_recipes?.length">
                <ul>
                  <li
                    v-for="r in recipe.parent_recipes"
                    :key="r.slug"
                    itemprop="recipeIngredient"
                  >
                    <Link
                      :href="t('routes.recipe_details', { slug: r.slug })"
                      class="underline"
                    >
                      {{ r.name }}
                    </Link>
                  </li>
                </ul>
              </div>
              <IngredientList
                :ingredients="ingredients"
                :groups="recipe.ingredient_groups"
              />
            </template>
          </Card>
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
