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
import RecipeComments from "@/components/RecipeComments.vue";
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
const isAboveMedium = breakpoints.greater("md");

const { share, canShare } = useShare();
const shareRecipe = async () => {
  await share(props.recipe.name, t("recipe.share_title", { name: props.recipe.name }));
};
</script>

<template>
  <head-section :title="recipe.name" />
  <div
    class="container mx-auto px-4"
    itemscope
    itemtype="https://schema.org/Recipe"
  >
    <div class="grid grid-cols-12 gap-4">
      <div class="col-span-12 md:col-span-8">
        <div class="flex flex-wrap sm:flex-nowrap items-center mb-2 md:mb-4">
          <h1
            class="text-2xl pt-2 grow w-full sm:w-auto"
            itemprop="name"
            :style="`view-transition-name: recipe-${recipe.slug}-name`"
          >
            {{ recipe.name }}
          </h1>
          <div class="grow sm:grow-0">
            <rating-form
              :average-rating="recipe.avg_rating"
              :num-ratings="recipe.num_ratings"
              :user-rating="userRating"
              :disabled="!user"
              class="w-fit"
            />
          </div>
          <favourite-form
            v-if="user"
            :user-favourite="userFavourite"
          />
          <button
            v-if="canShare"
            title="t('recipe.share')"
            class="ml-1 btn-text"
            @click="shareRecipe"
          >
            <span class="icon-[ooui--share]"></span>
          </button>
        </div>
        <breadcrumb-bar
          :current="recipe.name"
          class="p-0"
        />
        <div
          v-if="recipe.image_url"
          class="overflow-clip card mt-4 sm:hidden"
        >
          <img
            :src="recipe.image_url"
            :alt="recipe.name"
            :style="`view-transition-name: recipe-${recipe.slug}-image`"
          />
        </div>
        <description-item
          v-if="recipe.categories"
          :label="t('recipe.categories')"
        >
          <span
            v-for="c in recipe.categories"
            :key="c.slug"
            class="mx-1 border rounded-md px-2 py-1"
          >
            {{ c.type.name }}: {{ c.name }}
          </span>
        </description-item>
        <description-item :label="t('recipe.yields')">
          <recipe-yield
            v-if="recipe.yield_unit && recipe.yield_amount"
            :amount="recipe.yield_amount"
            :unit="recipe.yield_unit"
            :servings="servings"
            :base-servings="recipe.servings || 1"
          />
          <span v-else>{{ t("recipe.servings", servings) }}</span>
        </description-item>
        <description-item :label="t('recipe.added_by')">
          <user-avatar :user="recipe.added_by" />
          <span class="pl-2">
            {{ recipe.added_by.id === user?.id ? t("users.me") : recipe.added_by.full_name }}
          </span>
        </description-item>
        <description-item
          v-if="recipe.source"
          :label="t('recipe.from')"
        >
          <recipe-source
            :source="recipe.source"
            :value="recipe.source_value"
          />
        </description-item>
        <div
          v-if="recipe.description"
          class="mt-2 pb-5"
          itemprop="description"
        >
          <div class="divider"></div>
          {{ recipe.description }}
        </div>
        <recipe-durations
          :prep-time="recipe.prep_time"
          :cook-time="recipe.cook_time"
          :total-time="recipe.total_time"
        />
        <nutritional-information
          v-if="recipe.nutrition && !isAboveMedium"
          :nutrition="recipe.nutrition"
          :servings="servings"
          class="mt-4"
        />
        <recipe-comments
          v-if="!isAboveMedium"
          :comments="recipe.comments"
          :collapse="true"
          class="mt-4"
        />
        <div class="mt-4">
          <div class="card p-4">
            <div class="card-title pb-2">
              <div class="flex flex-row items-center">
                <h2 class="text-xxl grow w-100 mr-2">{{ t("recipe.ingredients") }}</h2>
                <servings-form :servings="servings || 1" />
              </div>
            </div>
            <div class="card-body">
              <div v-if="recipe.parent_recipes?.length">
                <ul>
                  <li
                    v-for="r in recipe.parent_recipes"
                    :key="r.slug"
                    itemprop="recipeIngredient"
                  >
                    <Link
                      :href="t('routes.recipe_detail', { slug: r.slug })"
                      class="underline"
                    >
                      {{ r.name }}
                    </Link>
                  </li>
                </ul>
              </div>
              <ingredient-list
                :ingredients="ingredients"
                :groups="recipe.ingredient_groups"
              />
            </div>
          </div>
        </div>
      </div>
      <div class="col-span-12 md:col-span-4 row-span-2">
        <div
          v-if="recipe.image_url"
          class="overflow-clip card hidden sm:flex"
        >
          <img
            :src="recipe.image_url"
            :alt="recipe.name"
            class="w-full"
            :style="`view-transition-name: recipe-${recipe.slug}-image`"
          />
        </div>
        <nutritional-information
          v-if="recipe.nutrition && isAboveMedium"
          :nutrition="recipe.nutrition"
          :servings="servings"
          class="mt-4"
        />
        <recipe-comments
          v-if="isAboveMedium"
          class="mt-4"
          :comments="recipe.comments"
        />
      </div>
      <div class="col-span-12 md:col-span-8">
        <div class="flex flex-row mb-2">
          <h2 class="text-xl grow">{{ t("recipe.directions") }}</h2>
          <keep-awake />
        </div>
        <div
          v-for="(step, i) in recipe.steps"
          :key="i"
          class="mb-2 mt-1 card p-2"
          itemprop="recipeInstructions"
        >
          <h3 class="card-title pb-2">{{ t("recipe.step_title", { step: i + 1 }) }}</h3>
          <p class="card-body">{{ step }}</p>
        </div>
      </div>
    </div>
  </div>
</template>
