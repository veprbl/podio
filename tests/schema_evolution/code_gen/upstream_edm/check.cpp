#include <datamodel/UpstreamComponentTypeCollection.h>

#include <upstream/UpstreamVector.h>

#include "check_base.h"

int main() {
  WRITE_AS(UpstreamComponentTypeCollection, {
    elem.position({1.5f, 2.5f, 3.5f});
    elem.oldName(42);
  });

  READ_AS(UpstreamComponentTypeCollection, {
    ASSERT_EQUAL(elem.newName(), 42, "Renamed member does not have the expected content");
    // The component comes from the upstream datamodel, which is versioned
    // independently, so it has to survive the evolution unchanged
    ASSERT_EQUAL(elem.position().x, 1.5f, "Upstream component member x does not have the expected content");
    ASSERT_EQUAL(elem.position().y, 2.5f, "Upstream component member y does not have the expected content");
    ASSERT_EQUAL(elem.position().z, 3.5f, "Upstream component member z does not have the expected content");
  });
}
